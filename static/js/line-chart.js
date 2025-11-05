var canvas = document.getElementById("line-chart");
var labels = JSON.parse(canvas.dataset.labels);
var data = JSON.parse(canvas.dataset.values);

var chart = new Chart(canvas, {
    type: "line",
    data: {
        labels: labels,
        datasets: [{
            label: "بازدید",
            data: data,
            backgroundColor: "rgba(56, 127, 12, 0.05)",
            borderColor: "#38BB0C",
            pointBorderColor: "#ffffff",
            pointBackgroundColor: "#38BB0C",
            pointBorderWidth: 2,
            pointRadius: 4
        }]
    },
    options: {
        plugins: {
            legend: { display: false },
            tooltip: { rtl: true, padding: 12 }
        },
        scales: {
            x: { grid: { color: "#eee" } },
            y: { grid: { color: "#eee" }, ticks: { font: { size: 14 } } }
        }
    }
});
