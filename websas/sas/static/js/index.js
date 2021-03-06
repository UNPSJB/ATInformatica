var chart
var chart_carga

function init_grafico_movimiento_mensual() {
    if ($("#chart-container")[0] === undefined){
        return
    }
    var fecha = moment() 
    var fecha_vieja = moment()
    var leyenda_comparacion = ""
    if($("#select-rango").val() == "anual"){
        fecha_vieja.subtract(1, "year")
        leyenda_comparacion = "Facturado en el año pasado"
    }
    else{
        fecha_vieja.subtract(1, "month")
        leyenda_comparacion = "Facturado en el mes pasado"
    }
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
                textoLeyenda: leyenda_comparacion,
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

function init_grafico_carga_trabajo() {

    if ($("#chart-container-carga-trabajo")[0] === undefined) {
        return
    }
    chart_carga = $("#chart-container-carga-trabajo").reporteSAS({
        opcionesDataset: [
            {
                tipochart: 'bar',
                x: 'criterio',
                y: 'cantidad_ots_abiertas',
                dataset: "carga_trabajo",
                textoLeyenda: "Carga de trabajo",
                opcionesAjax: {
                    ajaxurl: $("#chart-container-carga-trabajo")[0].dataset["ajax_url"],
                    filtro: $("#id_filtros").val(),
                },
            },
        ],
        opcionesGrafico: {
            // titulo: "Carga de Trabajo",
            nombre_eje_x: "Criterio",
            intervalo_eje_y: 5,
        }
    });
}
$(document).on('ready', function(){
    init_grafico_carga_trabajo()
    return init_grafico_movimiento_mensual()

})

$("#select-rango").on("change", function(){
    chart.CanvasJSChart().destroy()
    return init_grafico_movimiento_mensual()
})

$("form .chart-input").on("change", function(){
    chart.CanvasJSChart().destroy()
    return init_grafico_movimiento_mensual()
})

$('.chart-input-carga').on('change', function(){
    chart_carga.CanvasJSChart().destroy()
    return init_grafico_carga_trabajo()
})

$("#daterangepicker").on("apply.daterangepicker", function(ev, picker){
    chart.CanvasJSChart().destroy()
    return init_grafico_movimiento_mensual()
})
