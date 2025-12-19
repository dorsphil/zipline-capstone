document.addEventListener("DOMContentLoaded", () => {
    // Check if Chart.js loaded correctly from the CDN
    if (typeof Chart === 'undefined') {
        console.error("Chart.js library not loaded. Check your internet connection or CDN link.");
        return;
    }

    // --- Facility Coverage (Bar Chart) ---
    fetch("/data/processed/facilities_by_type.json")
        .then(res => {
            if (!res.ok) throw new Error(`Facilities JSON not found: ${res.status}`);
            return res.json();
        })
        .then(data => {
            console.log("Facilities Data:", data); // Debugging
            const ctx = document.getElementById("facilityTypeChart");
            if (!ctx) return;

            new Chart(ctx, {
                type: "bar",
                data: {
                    labels: data.map(d => d.facility_type),
                    datasets: [{
                        label: "Number of Facilities",
                        data: data.map(d => d.number_of_facilities),
                        backgroundColor: "#c62828"
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            });
        })
        .catch(err => console.error("Error loading Facility chart:", err));

    // --- Regions Served (Pie Chart) ---
    fetch("/data/processed/deliveries_by_region.json")
        .then(res => {
            if (!res.ok) throw new Error(`Regions JSON not found: ${res.status}`);
            return res.json();
        })
        .then(data => {
            console.log("Regions Data:", data); // Debugging
            const ctx = document.getElementById("regionChart");
            if (!ctx) return;

            new Chart(ctx, {
                type: "pie",
                data: {
                    labels: data.map(d => d.region),
                    datasets: [{
                        data: data.map(d => d.delivery_count),
                        backgroundColor: ["#c62828", "#e53935", "#ef5350", "#f44336", "#ef9a9a"]
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            });
        })
        .catch(err => console.error("Error loading Regions chart:", err));

    // --- District Table ---
    fetch("/data/processed/deliveries_by_district.json")
        .then(res => res.json())
        .then(data => {
            const tbody = document.querySelector("#districtTable tbody");
            if (!tbody) return;
            tbody.innerHTML = ""; // Clear "Loading"
            data.forEach(d => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${d.district}</td>
                    <td>${d.total_deliveries.toLocaleString()}</td>
                    <td>${d.pct_of_total_deliveries}%</td>
                `;
                tbody.appendChild(row);
            });
        })
        .catch(err => console.error("Error loading Table:", err));
});
