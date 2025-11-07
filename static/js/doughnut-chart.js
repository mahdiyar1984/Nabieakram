var ctx = document.getElementById("doughnut-chart");
if (!ctx) {
    console.warn("doughnut-chart canvas not found — skipping chart rendering.");
} else {
    Chart.defaults.global.defaultFontFamily = "Arial";
    Chart.defaults.global.defaultFontSize = 14;
    Chart.defaults.global.defaultFontStyle = "500";
    Chart.defaults.global.defaultFontColor = "#233d63";

    var chart = new Chart(ctx, {
        type: "doughnut",
        data: {
            datasets: [{
                data: [40, 32, 15],
                backgroundColor: ["#7E3CF9", "#F68A03", "#358FF7"],
                hoverBorderWidth: 5,
                hoverBorderColor: "#eee",
                borderWidth: 3
            }],
            labels: ["آموزش استانی", "آموزش شهرستانی", "آموزش دهستانی"]
        },
        options: {
            responsive: true,
            tooltips: { xPadding: 15, yPadding: 15, backgroundColor: "#2e3d62" },
            legend: { display: false },
            cutoutPercentage: 60
        }
    });

    var myLegendContainer = document.getElementById("legend");
    if (myLegendContainer) {
        myLegendContainer.innerHTML = chart.generateLegend();
        var legendItems = myLegendContainer.getElementsByTagName("li");
        for (var i = 0; i < legendItems.length; i++) {
            legendItems[i].addEventListener("click", legendClickCallback, false);
        }
    }

    function legendClickCallback(e) {
        e = e || window.event;
        var t = e.target || e.srcElement;
        while (t && t.nodeName !== "LI") {
            t = t.parentElement;
        }
        if (!t) return;
        var a = t.parentElement;
        var l = parseInt(a.classList[0].split("-")[0], 10);
        var n = Chart.instances[l];
        var d = Array.prototype.slice.call(a.children).indexOf(t);
        var r = n.getDatasetMeta(0).data[d];
        if (r) {
            if (r.hidden === null || r.hidden === false) {
                r.hidden = true;
                t.classList.add("hidden");
            } else {
                t.classList.remove("hidden");
                r.hidden = null;
            }
            n.update();
        }
    }
}
