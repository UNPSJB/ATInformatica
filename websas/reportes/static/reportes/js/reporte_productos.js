$(document).ready(function(){
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
    var fecha_ini = $("#daterangepicker").data('daterangepicker').startDate
    var fecha_fin = $("#daterangepicker").data('daterangepicker').endDate
    $("#comparacion-filtro").html("Comparación de utilización de productos por " + 
    $("form").find("select option:selected").text())
    $("#comparacion-mano-obra").html("Comparación de facturación por MDO y productos")
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

    $("#chart-cantidades").reporteSAS({
        opcionesDataset: [
            {
                tipochart: 'doughnut',
                x: 'criterio',
                y: 'cantidad',
                dataset: "cantidad_productos",
                // textoLeyenda: "Facturado en el año actual",
                opcionesAjax: {
                    fecha_ini: fecha_ini.format("DD/MM/YYYY"),
                    fecha_fin: fecha_fin.format("DD/MM/YYYY"),
                    filtro: $("#id_filtros").val(),
                    ajaxurl: $("form")[0].dataset["ajax_url_cantidad"],
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
    $("#chart-porcentajes").CanvasJSChart({
        
        data: [
            {
                type: "doughnut",
                showInLegend: true,
                dataPoints: [
                    { label: "Mano de obra", name: "Mano de obra", y: total_facturado },
                    { label: "Productos", name: "Productos", y: total_facturado_productos },
                ],
            },
        ],
    })
}
