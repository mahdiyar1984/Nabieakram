var ctx = document.getElementById("bar-chart");
if (ctx) {
    // فقط اگر canvas وجود داره، ادامه بده
    Chart.defaults.global.defaultFontFamily = "iransans";
    Chart.defaults.global.defaultFontSize = 14;
    Chart.defaults.global.defaultFontStyle = "500";
    Chart.defaults.global.defaultFontColor = "#233d63";

    var chart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: ["دی", "آذر", "آبان", "مهر", "شهریور", "مرداد", "تیر"],
            datasets: [{
                label: "فروش این ماه",
                data: [34, 41, 48, 45, 53, 55, 50],
                backgroundColor: "rgba(108, 92, 231, .2)",
                hoverBackgroundColor: "rgba(108, 92, 231, .6)",
                hoverBorderColor: "rgba(108, 92, 231, .6)",
                borderColor: "#7E3CF9",
                pointBackgroundColor: "#fff",
                borderWidth: 1,
            }],
        },
        options: {
            tooltips: { xPadding: 12, yPadding: 12, backgroundColor: "#2e3d62" },
            legend: { display: false },
            scales: {
                xAxes: [{ display: true, gridLines: { color: "transparent" } }],
                yAxes: [{ display: true, gridLines: { color: "transparent" }, ticks: { fontSize: 14 } }],
            },
        },
    });
} else {
    console.warn("bar-chart canvas not found — skipping chart rendering.");
}
