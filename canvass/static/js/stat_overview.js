$(function () {
    var upr_ctx = $("#usersPerRelease").get(0).getContext("2d");
    var upr_options = {
        legendTemplate : "<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<segments.length; i++){%><li><span style=\"color:<%=segments[i].fillColor%>; font-weight: bold;\"><%if(segments[i].label){%><%=segments[i].label%><%}%></li><%}%></span></ul>"
    };
    var upr_chart = new Chart(upr_ctx).Pie(upr_data, upr_options);
    var upr_legend = upr_chart.generateLegend();
    $("#upr_legend").html(upr_legend);

    var uma_ctx = $("#usersPerArch").get(0).getContext("2d");
    var uma_options = {
        legendTemplate : "<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<segments.length; i++){%><li><span style=\"color:<%=segments[i].fillColor%>; font-weight: bold;\"><%if(segments[i].label){%><%=segments[i].label%><%}%></li><%}%></span></ul>"
    };
    var uma_chart = new Chart(uma_ctx).Pie(uma_data, uma_options);
    var uma_legend = uma_chart.generateLegend();
    $("#uma_legend").html(uma_legend);
});
