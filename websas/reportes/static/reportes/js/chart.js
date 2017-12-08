var chart
var cantidad_chart

var COLORES = {    
    "dark_blue": "#3c6489",
    "light_blue": "#36A2FF",
    "blue_line": "#172d44",
    "paleta_1": "#FFE74C",
    "paleta_2": "#FF5964", 
    "paleta_3": "#F0B67F", 
    "paleta_4": "#38618C",
}
function init_chart(){


    if(chart){
        chart.destroy()
    }
    if(cantidad_chart){
        cantidad_chart.destroy()
    }

    var dataset_total_facturado = {
        label: 'Total facturado',
        data: [],
        backgroundColor: COLORES["light_blue"],
        borderColor: COLORES["blue_line"],
        borderWidth: 1,
        yAxisID: "total_facturado_y",
    } 

    var dataset_total_viejo = {
        label: 'Total facturado en el año anterior',
        data: [],
        backgroundColor: COLORES["dark_blue"],
        borderColor: COLORES["blue_line"],
        borderWidth: 1,
        yAxisID: "total_viejo_y",
    } 

    var data_total_ots = {
        labels: [],
        datasets: [dataset_total_facturado, dataset_total_viejo],
    }

    var opcioes_total_ots = {
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
                id: "total_viejo_y",
                display: false,
                ticks: {
                    beginAtZero:true,
                    //stepSize: 1,
                },
            },]
        },
    }

    chart = new Chart($("#chart-total-ots"), {
        type: 'bar',
        data: data_total_ots,
        options: opcioes_total_ots,
    });



    //inicializamos grafico de cantidades
    var dataset_cantidad_ots = {
        label: 'Cantidad de órdenes de trabajo',
        data: [],
        backgroundColor: [],
        borderColor: COLORES["blue_line"],
        borderWidth: 3,
    }

    var data_cantidad_ots = {
        labels: [],
        datasets: [dataset_cantidad_ots],
    }

    cantidad_chart = new Chart($("#chart-cantidad-ots"),{
        type: 'doughnut',
        data: data_cantidad_ots,
        options: Chart.defaults.doughnut,
    });

}

function displayBarLegend(barChart, legendId){
    var legend = "<ul>"
    for(let i=0; i<barChart.data.datasets.length; i++){
        const label = barChart.data.datasets[i].label
        const color = barChart.data.datasets[i].backgroundColor
        legend = legend + "<li><div id='rectangle' style='background:"
            + color + "'></div> <span>" + label + "</span></li><br/>"
    }
    legend = legend + "</ul>"
    $(legendId).html(legend)
}

function displayDoughnutLegend(doughnut, legendId){
    var legend = "<ul>"
    var data_total = 0
    for(let i=0; i<doughnut.data.datasets[0].data.length; i++){
        data_total += doughnut.data.datasets[0].data[i]
    }

    for(let i=0; i<doughnut.data.labels.length; i++){
        const label = doughnut.data.labels[i] + " (" +
            doughnut.data.datasets[0].data[i] + "/" +
            data_total + ")"
        const color = doughnut.data.datasets[0].backgroundColor[i]
        legend = legend + "<li><div id='rectangle' style='background:"
            + color + "'></div> <span>" + label + "</span></li><br/>"
    }
    legend = legend + "</ul>"
    console.log(legend)
    $(legendId).html(legend)
}
