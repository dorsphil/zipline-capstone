fetch("/data/processed/overview_kpis.json")
    .then(response => response.json())
    .then(data => {
        document.getElementById("totalDeliveries").textContent =
            data.total_deliveries.toLocaleString();

        document.getElementById("totalFacilities").textContent =
            data.total_facilities_served.toLocaleString();

        document.getElementById("peopleReached").textContent =
            data.estimated_people_reached.toLocaleString();
    })
    .catch(error => {
        console.error("Error loading overview data:", error);
    });
