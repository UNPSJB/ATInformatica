var chart
var cantidad_chart
var chartBar

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


    //if(cantidad_chart){
        //cantidad_chart.destroy()
    //}


    ////inicializamos grafico de cantidades
    //var dataset_cantidad_ots = {
        //label: 'Cantidad de órdenes de trabajo',
        //data: [],
        //backgroundColor: [],
        //borderColor: COLORES["blue_line"],
        //borderWidth: 3,
    //}

    //var data_cantidad_ots = {
        //labels: [],
        //datasets: [dataset_cantidad_ots],
    //}

    //cantidad_chart = new Chart($("#chart-cantidad-ots"),{
        //type: 'doughnut',
        //data: data_cantidad_ots,
        //options: Chart.defaults.doughnut,
    //});

    chartBar = $("#chart-totales").CanvasJSChart({
        title:{
            text: "Total facturado"              
        },
        legend: {
            horizontalAlign: "central",
            verticalAlign: "bottom",
            fontSize: 15,
        },
        data: [{        
                type: "column",
                showInLegend: true,
                legendText: "Total facturado en el año actual",
                dataPoints: [],
              },
              {        
                type: "column",
                showInLegend: true,
                legendText: "Total facturado en el año anterior",
                dataPoints: [],
              },        
          ],
    });


    chartBar = $("#chart-cantidades").CanvasJSChart({
        title:{
            text: "Cantidad de órdenes de trabajo"              
        },
        legend: {
            horizontalAlign: "central",
            verticalAlign: "bottom",
            fontSize: 15,
        },
        data: [{        
                type: "doughnut",
                showInLegend: true,
                dataPoints: [],
              },
          ],
    });

}

//function displayBarLegend(barChart, legendId){
    //var legend = "<ul>"
    //for(let i=0; i<barChart.data.datasets.length; i++){
        //const label = barChart.data.datasets[i].label
        //const color = barChart.data.datasets[i].backgroundColor
        //legend = legend + "<li><div id='rectangle' style='background:"
            //+ color + "'></div> <span>" + label + "</span></li><br/>"
    //}
    //legend = legend + "</ul>"
    //$(legendId).html(legend)
//}

//function displayDoughnutLegend(doughnut, legendId){
    //var legend = "<ul>"
    //var data_total = 0
    //for(let i=0; i<doughnut.data.datasets[0].data.length; i++){
        //data_total += doughnut.data.datasets[0].data[i]
    //}

    //for(let i=0; i<doughnut.data.labels.length; i++){
        //const label = doughnut.data.labels[i] + " (" +
            //doughnut.data.datasets[0].data[i] + "/" +
            //data_total + ")"
        //const color = doughnut.data.datasets[0].backgroundColor[i]
        //legend = legend + "<li><div id='rectangle' style='background:"
            //+ color + "'></div> <span>" + label + "</span></li><br/>"
    //}
    //legend = legend + "</ul>"
    ////console.log(legend)
    //$(legendId).html(legend)
//}
