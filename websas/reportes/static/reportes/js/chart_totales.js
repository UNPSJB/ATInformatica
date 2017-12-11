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
