// =====================================
// Product Types Delivered (bar chart)
// =====================================
fetch("../../data/processed/products_by_category.json")
    .then(res => res.json())
    .then(data => {
        new Chart(document.getElementById("productsCategoryChart"), {
            type: "bar",
            data: {
                labels: data.map(d => d.use_case_category),
                datasets: [{
                    label: "Total Deliveries",
                    data: data.map(d => d.total_deliveries),
                    minBarLength: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    });


// =====================================
// Emergency Product Types (table)
// =====================================
fetch("../../data/processed/emergency_products.json")
    .then(res => res.json())
    .then(data => {
        const tbody = document.querySelector("#emergencyProductsTable tbody");

        data.forEach(d => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${d.use_case_category}</td>
                <td>${d.use_case_subcategory}</td>
                <td>${d.emergency_delivery_count}</td>
            `;
            tbody.appendChild(row);
        });
    });


// =====================================
// Avg Delivery Time by Product (bar)
// =====================================
fetch("../../data/processed/avg_delivery_time_by_product.json")
    .then(res => res.json())
    .then(data => {
        new Chart(document.getElementById("avgDeliveryTimeChart"), {
            type: "bar",
            data: {
                labels: data.map(d => d.use_case_category),
                datasets: [{
                    label: "Avg Delivery Time (minutes)",
                    data: data.map(d => d.avg_delivery_time_minutes)
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    });
