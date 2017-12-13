var chart

function init_grafico() {
    if($("form")[0] === undefined){
        return
    }
    var fecha_ini = $("#daterangepicker").data('daterangepicker').startDate
    var fecha_fin = $("#daterangepicker").data('daterangepicker').endDate

    //copiamos las fechas porque si no se va a decrementando en un anio
    //cada vez que se envia el segundo dataset
    var fecha_ini_vieja = moment($("#daterangepicker").data('daterangepicker').startDate)
    var fecha_fin_vieja = moment($("#daterangepicker").data('daterangepicker').endDate)

    $("#fecha-ini").html(fecha_ini.format("DD/MM/YYYY"))
    $("#fecha-fin").html(fecha_fin.format("DD/MM/YYYY"))
    chart = $("#chart-container").reporteSAS({
        opcionesDataset: [
            {
                tipochart: 'column',
                x: '0',
                y: '1',
                dataset: "ordenes_total",
                textoLeyenda: "Facturado en el año actual",
                opcionesAjax: {
                    fecha_ini: fecha_ini.format("DD/MM/YYYY"),
                    fecha_fin: fecha_fin.format("DD/MM/YYYY"),
                    filtro: $("#id_filtros").val(),
                    ajaxurl: $("form")[0].dataset["ajax_url"],
                },
            },
            {
                tipochart: 'column',
                x: '0',
                y: '1',
                dataset: "ordenes_total",
                textoLeyenda: "Facturado en el año pasado",
                opcionesAjax: {
                    fecha_ini: fecha_ini_vieja.subtract(1, "year").format("DD/MM/YYYY"),
                    fecha_fin: fecha_fin_vieja.subtract(1, "year").format("DD/MM/YYYY"),
                    filtro: $("#id_filtros").val(),
                    ajaxurl: $("form")[0].dataset["ajax_url"],
                },
            },
        ],
        opcionesGrafico: {}
    });
}
$(document).on('ready', function () {
    return init_grafico()
})

$("form .chart-input").on("change", function () {
    chart.CanvasJSChart().destroy()
    return init_grafico()
})


$("#daterangepicker").on("apply.daterangepicker", function (ev, picker) {
    chart.CanvasJSChart().destroy()
    return init_grafico()
})
