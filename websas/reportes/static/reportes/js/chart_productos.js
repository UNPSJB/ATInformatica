$(document).on("ready", function () {
    var chartBar = new CanvasJS.Chart("chartBar", {
        title:{
            text: "Unas columnitas (el de barras es el horizontal, ojota)"              
        },
        data: [{        
            
                type: "column",
                dataPoints: [
                { x: 10, y: 171 },
                { x: 20, y: 155},
                { x: 30, y: 150 },
                { x: 40, y: 165 },
                { x: 50, y: 195 },
                { x: 60, y: 168 },
                { x: 70, y: 128 },
                { x: 80, y: 134 },
                { x: 90, y: 114}
                ]
              },
              {        
                type: "column",
                dataPoints: [
                { x: 10, y: 71 },
                { x: 20, y: 55},
                { x: 30, y: 50 },
                { x: 40, y: 65 },
                { x: 50, y: 95 },
                { x: 60, y: 68 },
                { x: 70, y: 28 },
                { x: 80, y: 34 },
                { x: 90, y: 14}
                ]
              }        
              ],
    });
    chartBar.render();

    var chartDoughnut = new CanvasJS.Chart("chartDoughnut", {
        title:{
            text: "La torta"              
        },
        data: [              
        {
            // Change type to "doughnut", "line", "splineArea", etc.
            type: "doughnut",
            dataPoints: [
                { label: "apple",  y: 10  },
                { label: "orange", y: 15  },
                { label: "banana", y: 25  },
                { label: "mango",  y: 30  },
                { label: "grape",  y: 28  }
            ]
        }
        ]
    });
    chartDoughnut.render()

    //otra forma de hacer, con los selectores de jQuery
    var chartArea = $("#chartArea").CanvasJSChart({
        title:{
            text: "Con selectores de jQuery"              
        },
        data: [              
        {
            // Change type to "doughnut", "line", "splineArea", etc.
            type: "area",
            dataPoints: [
                { label: "apple",  y: 10  },
                { label: "orange", y: 15  },
                { label: "banana", y: 25  },
                { label: "mango",  y: 30  },
                { label: "grape",  y: 28  }
            ]
        }
        ]
    });
})
