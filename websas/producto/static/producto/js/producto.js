var tabla_html = $("#datatable-producto");

var botones_default = [{
    extend: "copy",
    text: "Copiar tabla",
    className: "btn-sm"
}, {
    extend: "csv",
    text: "Exportar tabla a CSV",
    className: "btn-sm"
}, {
    extend: "print",
    text: "Imprimir tabla",
    className: "btn-sm"
}];

var botones_dt;

if (tabla_html.attr('data-url_agregar')) {
    var boton_agregar = [{
        text: "<b>Nuevo producto</b>",
        action: function() {
            location.href = tabla_html.attr('data-url_agregar');
        },
        className: "btn-sm btn-info"
    }]

    botones_dt = boton_agregar.concat(botones_default);
} else {
    botones_dt = botones_default;
}

tabla_html.DataTable({
    responsive: true,
    dom: "Bfrtip",
    buttons: botones_dt,
});

$(document).ready(function () {
    inicializarGrafico()
})

$("form").on("change", function () {
    inicializarGrafico()
})

$("#daterangepicker").on("apply.daterangepicker", function (ev, picker) {
    inicializarGrafico()
    /**
     * Esta es otra forma de manejar el mismo evento que con el callback que se le paso en el constructor
     */

})

function inicializarGrafico() {
    if($("form")[0] === undefined){
        return
    }
    var fecha_ini = $("#daterangepicker").data('daterangepicker').startDate
    var fecha_fin = $("#daterangepicker").data('daterangepicker').endDate
    $("#fecha-ini").html(fecha_ini.format("DD/MM/YYYY"))
    $("#fecha-fin").html(fecha_fin.format("DD/MM/YYYY"))

    var chart = $("#chart-totales-productos").reporteSAS({
        opcionesDataset: [
            {
                tipochart: 'bar',
                x: '0',
                y: '1',
                dataset: "ordenes_total",
                textoLeyenda: "Total facturado",
                opcionesAjax: {
                    fecha_ini: fecha_ini.format("DD/MM/YYYY"),
                    fecha_fin: fecha_fin.format("DD/MM/YYYY"),
                    filtro: $("#id_filtros").val(),
                    ajaxurl: $("form")[0].dataset["ajax_url_total"],
                },
            },
            {
                tipochart: 'bar',
                x: 'criterio',
                y: 'incidencia',
                dataset: "incidencia_productos",
                textoLeyenda: "Incidencia de los productos",
                opcionesAjax: {
                    fecha_ini: fecha_ini.format("DD/MM/YYYY"),
                    fecha_fin: fecha_fin.format("DD/MM/YYYY"),
                    filtro: $("#id_filtros").val(),
                    ajaxurl: $("form")[0].dataset["ajax_url"],
                },
            },
        ],
        opcionesGrafico: {}
    });

    var chart_totales = $("#chart-totales-productos").CanvasJSChart()
    var total_facturado = 0
    var total_facturado_productos = 0
    for (let i = 0; i < chart_totales.options.data[0].dataPoints.length; i++) {
        const element = chart_totales.options.data[0].dataPoints[i];
        total_facturado += parseInt(element["y"])
    }
    $("#total").html("$ " + total_facturado)
    for (let i = 0; i < chart_totales.options.data[1].dataPoints.length; i++) {
        const element = chart_totales.options.data[1].dataPoints[i];
        total_facturado_productos += parseInt(element["y"])
    }
    $("#total-productos").html("$ " + total_facturado_productos)
}
