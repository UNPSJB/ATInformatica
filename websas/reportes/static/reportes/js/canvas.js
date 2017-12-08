$(document).on("ready", function () {
    var chartBar = new CanvasJS.Chart("chartBar", {
        title:{
            text: "Unas columnitas (el de barras es el horizontal, ojota)"              
        },
        data: [              
        {
            // Change type to "doughnut", "line", "splineArea", etc.
            type: "column",
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
    //es opcional el render si lo haces con los selectores de jQuery pareceria
    //chartArea.render()
})
