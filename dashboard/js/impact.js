// ===============================
// Facility coverage (bar chart)
// ===============================
fetch("/dashboard/data/processed/facilities_by_type.json")
    .then(res => res.json())
    .then(data => {
        new Chart(document.getElementById("facilityTypeChart"), {
            type: "bar",
            data: {
                labels: data.map(d => d.facility_type),
                datasets: [{
                    label: "Number of Facilities",
                    data: data.map(d => d.number_of_facilities)
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    });


// ===============================
// Regions served (pie chart)
// ===============================
fetch("/dashboard/data/processed/deliveries_by_region.json")
    .then(res => res.json())
    .then(data => {
        new Chart(document.getElementById("regionChart"), {
            type: "pie",
            data: {
                labels: data.map(d => d.region),
                datasets: [{
                    data: data.map(d => d.delivery_count)
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    });


// ===============================
// District-level beneficiaries (table)
// ===============================
fetch("/dashboard/data/processed/deliveries_by_district.json")
    .then(res => res.json())
    .then(data => {
        const tbody = document.querySelector("#districtTable tbody");

        data.forEach(d => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${d.district}</td>
                <td>${d.total_deliveries}</td>
                <td>${d.pct_of_total_deliveries}%</td>
            `;
            tbody.appendChild(row);
        });
    });
