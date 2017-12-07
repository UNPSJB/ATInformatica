var chart;

//var light_blue = "rgba(54, 162, 255, 0.5)"
var light_blue = "#c7d66d"
var dark_blue = "rgba(60, 100, 137, 1)"
var blue_line = "rgba(23, 45, 68, 1)"

var colors = ["#36A2FF", "#FFE74C", "#FF5964", "#F0B67F", "#38618C"]
function init_chart(){


    if(chart){
        chart.destroy()
    }

    var dataset_total_facturado = {
        label: 'Total facturado',
        data: [],
        backgroundColor: light_blue,
        borderColor: blue_line,
        borderWidth: 1,
        yAxisID: "total_facturado_y",
    } 

    var dataset_cantidad = {
        label: 'Cantidad de órdenes de trabajo',
        data: [],
        backgroundColor: dark_blue,
        borderColor: blue_line,
        borderWidth: 1,
        yAxisID: "cantidad_y",
    } 

    var data_ots_clientes = {
        labels: [],
        datasets: [dataset_total_facturado, dataset_cantidad],
    }

    var opciones_ots_clientes = {
        legend: Chart.defaults.global.legend,
        scales: {
            xAxes: [{
                barPercentage: 1,
                categoryPercentage: 0.6,
            },],
            yAxes: [{
                id: "total_facturado_y",
                ticks: {
                    beginAtZero:true,
                },
            }, {
                id: "cantidad_y",
                position: "right",
                ticks: {
                    beginAtZero:true,
                    stepSize: 1,
                },
            },]
        },
    }

    chart = new Chart($("#chart-ots-clientes"), {
        type: 'bar',
        data: data_ots_clientes,
        options: opciones_ots_clientes,
    });

    $("#chart-legend").html(chart.generateLegend())
}


var myPieChart = new Chart($("#chart-ots-tecnicos"),{
    type: 'doughnut',
    data: {
        datasets: [{
            data: [10, 20, 30, 15],
            backgroundColor: ['red', 'yellow', 'blue', "white"],
        }],
        // These labels appear in the legend and in the tooltips when hovering different arcs
        labels: [
            'Red',
            'Yellow',
            'Blue',
            'White',
        ]
    },
    options: Chart.defaults.doughnut,
    });


$("#chart-container-tecnicos").show()
