var chart

function init_grafico() {
    var fecha = moment() 
    var fecha_vieja = moment().subtract(1, "year")

    chart = $("#chart-container").reporteSAS({
        opcionesDataset: [
            {
                tipochart: 'splineArea',
                x: '0',
                y: '1',
                dataset: "facturacion",
                textoLeyenda: "Facturado en el año actual",
                opcionesAjax: {
                    fecha_ini: fecha.format("DD/MM/YYYY"),
                    ajaxurl: $("#chart-container")[0].dataset["ajax_url"],
                },
            },
            {
                tipochart: 'splineArea',
                x: '0',
                y: '1',
                dataset: "facturacion",
                textoLeyenda: "Facturado en el año pasado",
                opcionesAjax: {
                    fecha_ini: fecha_vieja.format("DD/MM/YYYY"),
                    ajaxurl: $("#chart-container")[0].dataset["ajax_url"],
                },
            },
        ],
        opcionesGrafico: {
            titulo: "Facturación diaria",
            nombre_eje_x: "Días del mes",
        }
    });
}
$(document).on('ready', function(){
    return init_grafico()
})

$("form .chart-input").on("change", function(){
    chart.CanvasJSChart().destroy()
    return init_grafico()
})


$("#daterangepicker").on("apply.daterangepicker", function(ev, picker){
    chart.CanvasJSChart().destroy()
    return init_grafico()
})
