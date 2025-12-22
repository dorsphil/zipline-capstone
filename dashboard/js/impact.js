Chart.register(ChartDataLabels);

// ===============================
// Deliveries by Facility Type (Vertical Bar Chart)
// ===============================
fetch("/data/processed/deliveries_by_facility_type.json")
    .then(res => res.json())
    .then(data => {
        new Chart(document.getElementById("facilityDeliveriesChart"), {
            type: "bar",
            data: {
                labels: data.map(d => d.facility_type),
                datasets: [{
                    label: "Total Deliveries",
                    data: data.map(d => d.total_deliveries),
                    backgroundColor: data.map((_, i) => `rgba(0, 150, 136, ${1 - (i / data.length) * 0.7})`),
                    borderColor: 'rgb(0, 150, 136)',
                    borderWidth: 1,
                    borderRadius: 0 
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                layout: {
                    padding: {
                        top: 30,
                        bottom: 10 // Added space for X-axis label
                    }
                },
                scales: {
                    x: {
                        grid: { display: false },
                        // ADDED X-AXIS LABEL
                        title: {
                            display: true,
                            text: 'Facility Type',
                            font: { weight: 'bold' }
                        }
                    },
                    y: {
                        display: true,
                        grid: { display: false },
                        border: { display: true },
                        // ADDED Y-AXIS LABEL
                        title: {
                            display: true,
                            text: 'Total Deliveries',
                            font: { weight: 'bold' }
                        },
                        ticks: {
                            font: { weight: "bold" }
                        }
                    }
                },
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: ctx =>
                                `${ctx.raw} deliveries (${data[ctx.dataIndex].pct_of_total_deliveries}%)`
                        }
                    },
                    datalabels: {
                        anchor: "end",
                        align: "end",
                        formatter: (value, ctx) =>
                            `${data[ctx.dataIndex].pct_of_total_deliveries}%`,
                        color: "#444",
                        font: {
                            weight: "bold",
                            size: 11
                        }
                    }
                }
            }
        });
    });

// ===============================
// Facility coverage (pie chart)
// ===============================
// (No changes needed - Pie charts do not have axes)
fetch("/data/processed/facilities_by_type.json")
    .then(res => res.json())
    .then(data => {
        const total = data.reduce((sum, d) => sum + d.number_of_facilities, 0);

        new Chart(document.getElementById("facilityTypeChart"), {
            type: "pie",
            data: {
                labels: data.map(d => d.facility_type),
                datasets: [{
                    data: data.map(d => d.number_of_facilities)
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                layout: {
                    padding: {
                        top: 80,
                        bottom: 40,
                        left: 80,
                        right: 80
                    }
                },
                plugins: {
            legend: {
                position: 'bottom',
                labels: {
                    padding: 20
                }
            },
                    tooltip: {
                        callbacks: {
                            label: ctx => {
                                const value = ctx.raw;
                                const pct = ((value / total) * 100).toFixed(1);
                                return `${value} facilities (${pct}%)`;
                            }
                        }
                    },
          datalabels: {
  formatter: (value) => {
    const pct = ((value / total) * 100).toFixed(1);
    return `${pct}%`;
  },
  color: (context) => {
    const pct = ((context.dataset.data[context.dataIndex] / total) * 100);
    return pct < 5 ? '#333' : '#fff';
  },
  anchor: (context) => {
    const pct = ((context.dataset.data[context.dataIndex] / total) * 100);
    return pct < 5 ? 'end' : 'center';
  },
  align: (context) => {
    const pct = ((context.dataset.data[context.dataIndex] / total) * 100);
    return pct < 5 ? 'end' : 'center';
  },
  offset: (context) => {
    const pct = ((context.dataset.data[context.dataIndex] / total) * 100);
    return pct < 5 ? 24 : 0;
  },
  font: {
    weight: "bold",
    size: 12
  },
  backgroundColor: (context) => {
    const pct = ((context.dataset.data[context.dataIndex] / total) * 100);
    return pct < 5 ? 'rgba(255, 255, 255, 0.9)' : 'transparent';
  },
  borderColor: (context) => {
    const pct = ((context.dataset.data[context.dataIndex] / total) * 100);
    return pct < 5 ? '#ccc' : 'transparent';
  },
  borderWidth: (context) => {
    const pct = ((context.dataset.data[context.dataIndex] / total) * 100);
    return pct < 5 ? 1 : 0;
  },
  borderRadius: 4,
  padding: (context) => {
    const pct = ((context.dataset.data[context.dataIndex] / total) * 100);
    return pct < 5 ? 4 : 0;
  }
}
    }
}
        }); 
    }); 

// ===============================
// Regions served (pie chart with % labels)
// ===============================
// (No changes needed - Pie charts do not have axes)
fetch("/data/processed/deliveries_by_region.json") 
    .then(res => res.json())
    .then(data => {
        const total = data.reduce((sum, d) => sum + d.delivery_count, 0);

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
                maintainAspectRatio: false,
                layout: {
                    padding: {
                        top: 80,
                        bottom: 40,
                        left: 80,
                        right: 80
                    }
                },
                plugins: {
        legend: {
            position: 'bottom',
            labels: {
                padding: 20
            }
        },
                    tooltip: {
                        callbacks: {
                            label: ctx => {
                                const value = ctx.raw;
                                const pct = ((value / total) * 100).toFixed(1);
                                return `${value} deliveries (${pct}%)`;
                            }
                        }
                    },
                datalabels: {
  formatter: (value) => {
    const pct = ((value / total) * 100).toFixed(1);
    return `${pct}%`;
  },
  color: (context) => {
    const pct = ((context.dataset.data[context.dataIndex] / total) * 100);
    return pct < 5 ? '#333' : '#fff';
  },
  anchor: (context) => {
    const pct = ((context.dataset.data[context.dataIndex] / total) * 100);
    return pct < 5 ? 'end' : 'center';
  },
  
  align: (context) => {
    const pct = ((context.dataset.data[context.dataIndex] / total) * 100);
    if (pct < 5) {
        const index = context.dataIndex;
        return index % 2 === 0 ? 'end' : 'start'; 
    }
    return 'center';
},

offset: (context) => {
    const pct = ((context.dataset.data[context.dataIndex] / total) * 100);
    if (pct < 5) {
        return context.dataIndex * 10 + 20; 
    }
    return 0;
},
 
  backgroundColor: (context) => {
    const pct = ((context.dataset.data[context.dataIndex] / total) * 100);
    return pct < 5 ? 'rgba(255, 255, 255, 0.9)' : 'transparent';
  },
  borderColor: (context) => {
    const pct = ((context.dataset.data[context.dataIndex] / total) * 100);
    return pct < 5 ? '#ccc' : 'transparent';
  },
  borderWidth: (context) => {
    const pct = ((context.dataset.data[context.dataIndex] / total) * 100);
    return pct < 5 ? 1 : 0;
  },
  borderRadius: 4,
  padding: (context) => {
    const pct = ((context.dataset.data[context.dataIndex] / total) * 100);
    return pct < 5 ? 4 : 0;
  }
}
            }
        }
        });
    });

// ===============================
// District-level beneficiaries (horizontal bar chart)
// ===============================
fetch("/data/processed/deliveries_by_district.json")
    .then(res => res.json())
    .then(data => {
        new Chart(document.getElementById("districtChart"), {
            type: "bar",
            data: {
                labels: data.map(d => d.district),
                datasets: [{
                    label: "Total Deliveries",
                    data: data.map(d => d.total_deliveries),
                    backgroundColor: data.map((_, i) => `rgba(0, 150, 136, ${1 - (i / data.length) * 0.7})`),
                    borderColor: 'rgb(0, 150, 136)',
                    borderWidth: 1,
                    borderRadius: 8,
                    borderSkipped: false,
                }]
            },
            options: {
                indexAxis: "y",
                responsive: true,
                maintainAspectRatio: false,
                layout: {
                    padding: {
                        right: 70,
                        top: 10,
                        bottom: 20 // Added space for X-axis label
                    }
                },
                scales: {
                    x: {
                        display: true, // Switched to true to show the label
                        grid: { display: false },
                        // ADDED X-AXIS LABEL (Volume)
                        title: {
                            display: true,
                            text: 'Total Deliveries',
                            font: { weight: 'bold' }
                        },
                        ticks: { display: false } // Keeping ticks hidden as requested before
                    },
                    y: {
                        grid: { display: false },
                        // ADDED Y-AXIS LABEL (Districts)
                        title: {
                            display: true,
                            text: 'Districts',
                            font: { weight: 'bold' }
                        },
                        ticks: {
                            font: { weight: 'bold' }
                        }
                    }
                },
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: ctx => `${ctx.raw} deliveries (${data[ctx.dataIndex].pct_of_total_deliveries}%)`
                        }
                    },
                    datalabels: {
                        anchor: "end",
                        align: "end",
                        formatter: (value, ctx) => `${data[ctx.dataIndex].pct_of_total_deliveries}%`,
                        color: "#444",
                        font: { weight: "bold", size: 11 }
                    }
                }
            }
        });
    });