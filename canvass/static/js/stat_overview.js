$(function () {
    var upr_ctx = $("#usersPerRelease").get(0).getContext("2d");
    var upr_data = [
        {
            value: 300,
            color:"#F7464A",
            highlight: "#FF5A5E",
            label: "Red"
        },
        {
            value: 50,
            color: "#46BFBD",
            highlight: "#5AD3D1",
            label: "Green"
        },
        {
            value: 100,
            color: "#FDB45C",
            highlight: "#FFC870",
            label: "Yellow"
        }
    ];
    var upr_chart = new Chart(upr_ctx).Pie(upr_data);
});
