var canvas = document.getElementById("line-chart");

// Decode unicode before parsing JSON
function decodeUnicode(str) {
    return str.replace(/\\u[\dA-F]{4}/gi, function (match) {
        return String.fromCharCode(parseInt(match.replace(/\\u/g, ''), 16));
    });
}

var labelsRaw = canvas.dataset.labels || "[]";
var dataRaw = canvas.dataset.values || "[]";

try {
    // decode Unicode escape sequences
    labelsRaw = decodeUnicode(labelsRaw);
    dataRaw = decodeUnicode(dataRaw);

    var labels = JSON.parse(labelsRaw);
    var data = JSON.parse(dataRaw);
} catch (e) {
    console.error("Error parsing chart data:", e);
    var labels = [];
    var data = [];
}

console.log(labels, data); // ببین آیا در console درست چاپ میشه

// رسم نمودار
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
