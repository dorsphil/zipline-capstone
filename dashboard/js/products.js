Chart.register(ChartDataLabels);

// =====================================
// Product Types Delivered (Vertical Bar)
// =====================================
fetch("../../data/processed/products_by_category.json")
    .then(res => res.json())
    .then(data => {
        const total = data.reduce((s, d) => s + d.total_deliveries, 0);

        new Chart(document.getElementById("productsCategoryChart"), {
            type: "bar",
            data: {
                labels: data.map(d => d.use_case_category),
                datasets: [{
                    label: "Total Deliveries",
                    data: data.map(d => d.total_deliveries),
                    minBarLength: 6,
                    borderRadius: 0,
                    backgroundColor: 'rgba(0, 150, 136, 0.8)',
                    borderColor: 'rgb(0, 150, 136)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { 
                        grid: { display: false },
                        // ADDED X-AXIS LABEL
                        title: {
                            display: true,
                            text: 'Product Category',
                            font: { weight: 'bold' }
                        }
                    },
                    y: { 
                        display: true,
                        grid: { display: false },
                        border: { display: true },
                        ticks: { display: true },
                        // ADDED Y-AXIS LABEL
                        title: {
                            display: true,
                            text: 'Total Deliveries',
                            font: { weight: 'bold' }
                        }
                    }
                },
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: ctx => {
                                const v = ctx.raw;
                                const pct = ((v / total) * 100).toFixed(1);
                                return `${v} deliveries (${pct}%)`;
                            }
                        }
                    },
                    datalabels: {
                        anchor: "end",
                        align: "end",
                        formatter: v => `${((v / total) * 100).toFixed(1)}%`,
                        font: { weight: "bold", size: 11 },
                        color: "#444"
                    }
                }
            }
        });
    });

// =====================================
// Emergency Product Types (HORIZONTAL)
// =====================================
fetch("../../data/processed/emergency_products.json")
    .then(res => res.json())
    .then(data => {
        const total = data.reduce((s, d) => s + d.emergency_delivery_count, 0);

        new Chart(document.getElementById("emergencyProductsChart"), {
            type: "bar",
            data: {
                labels: data.map(d => d.use_case_subcategory),
                datasets: [{
                    label: "Emergency Deliveries",
                    data: data.map(d => d.emergency_delivery_count),
                    borderRadius: 5,
                    borderSkipped: false,
                    backgroundColor: data.map((_, i) => `rgba(0, 150, 136, ${1 - (i / data.length) * 0.7})`),
                    borderColor: 'rgb(0, 150, 136)',
                    borderWidth: 1
                }]
            },
            options: {
                indexAxis: "y",
                responsive: true,
                maintainAspectRatio: false,
                layout: {
                    padding: { right: 60, bottom: 20 }
                },
                scales: {
                    x: { 
                        display: true, 
                        grid: { display: false },
                        ticks: { display: false },
                        // ADDED X-AXIS LABEL
                        title: {
                            display: true,
                            text: 'Delivery Volume',
                            font: { weight: 'bold' }
                        }
                    },
                    y: { 
                        grid: { display: false },
                        // ADDED Y-AXIS LABEL
                        title: {
                            display: true,
                            text: 'Product Type',
                            font: { weight: 'bold' }
                        }
                    }
                },
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: ctx => {
                                const v = ctx.raw;
                                const pct = ((v / total) * 100).toFixed(1);
                                return `${v} deliveries (${pct}%)`;
                            }
                        }
                    },
                    datalabels: {
                        anchor: "end",
                        align: "right",
                        formatter: v => `${((v / total) * 100).toFixed(1)}%`,
                        font: { weight: "bold", size: 10 },
                        color: "#444"
                    }
                }
            }
        });
    });

// =====================================
// Avg Delivery Time by Product (Vertical Bar)
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
                    data: data.map(d => d.avg_delivery_time_minutes),
                    borderRadius: 0,
                    backgroundColor: 'rgba(0, 150, 136, 0.6)',
                    borderColor: 'rgb(0, 150, 136)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                layout: {
                    padding: { bottom: 10 }
                },
                scales: {
                    x: { 
                        grid: { display: false },
                        // ADDED X-AXIS LABEL
                        title: {
                            display: true,
                            text: 'Product Category',
                            font: { weight: 'bold' }
                        }
                    },
                    y: { 
                        grid: { display: false },
                        // ADDED Y-AXIS LABEL
                        title: {
                            display: true,
                            text: 'Time (Minutes)',
                            font: { weight: 'bold' }
                        }
                    }
                },
                plugins: {
                    legend: { display: false },
                    datalabels: {
                        anchor: "end",
                        align: "end",
                        formatter: v => `${v.toFixed(1)} min`,
                        font: { weight: "bold", size: 11 },
                        color: "#444"
                    }
                }
            }
        });
    });