$(document).on('ready', function(){
    inicializarGrafico()
})

function inicializarGrafico() {
    var fecha_ini = $("#daterangepicker").data('daterangepicker').startDate
    var fecha_fin = $("#daterangepicker").data('daterangepicker').endDate

    //copiamos las fechas porque si no se va a decrementando en un anio
    //cada vez que se envia el segundo dataset
    var fecha_ini_vieja = moment($("#daterangepicker").data('daterangepicker').startDate)
    var fecha_fin_vieja = moment($("#daterangepicker").data('daterangepicker').endDate)

    $("#fecha-ini").html(fecha_ini.format("DD/MM/YYYY"))
    $("#fecha-fin").html(fecha_fin.format("DD/MM/YYYY"))
    var chart = $("#chart-totales").reporteSAS({
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
        opcionesGrafico: {
            titulo: "Facturado en el año actual y el año pasado",
        }
    });

    $("#chart-cantidades").reporteSAS({
        opcionesDataset: [
            {
                tipochart: 'doughnut',
                x: 'criterio',
                y: 'cantidad',
                dataset: "cantidad_ordenes",
                // textoLeyenda: "Facturado en el año actual",
                opcionesAjax: {
                    fecha_ini: fecha_ini.format("DD/MM/YYYY"),
                    fecha_fin: fecha_fin.format("DD/MM/YYYY"),
                    filtro: $("#id_filtros").val(),
                    ajaxurl: $("form")[0].dataset["ajax_url_cantidad"],
                },
            },
        ],
        opcionesGrafico: {
            titulo: "Cantidad de órdenes de trabajo por " + $("#id_filtros option:selected").text()
        }
    });

    var chart_totales = $("#chart-totales").CanvasJSChart()
    var total_facturado = 0
    for (let i = 0; i < chart_totales.options.data[0].dataPoints.length; i++) {
        const element = chart_totales.options.data[0].dataPoints[i];
        total_facturado += parseInt(element["y"])
    }
    $("#total").html("$ " + total_facturado)
    var panel_reporte = $('#reporte_pre').first();


    // Si no lo mostré todavía, mostrarlo.
    if (panel_reporte.css('display') == 'none') {
        panel_reporte.css('display', 'inline-block');
    }
    // Si está plegado, desplegarlo.
    if (panel_reporte.find('.x_content').first().css('display', 'none')) {
        panel_reporte.find('.collapse-link').first().trigger('click');
    }

}

// function inicializarGrafico () {
//     //inicializamos graficos
//     init_chart()

//     var total_facturado = 0
//     var picker = $("#daterangepicker").data('daterangepicker')
//     var fecha_ini = picker.startDate.format("DD/MM/YYYY")
//     var fecha_fin = picker.endDate.format("DD/MM/YYYY")
//     var filtro = $("#id_filtros").val()

//     $.ajax({
//         url: $("form")[0].dataset["ajax_url"],
//         type: "GET",
//         data: {
//             "fecha_ini": fecha_ini,
//             "fecha_fin": fecha_fin,
//             "filtros": filtro,
//         },
//         dataType: "json",
//         success: function(data){
//             console.log(data);
//             //Si la lista de ordenes viene vacia, mostramos el error

//             // Activar visualizador abajo
//             var chart_totales = $("#chart-totales").CanvasJSChart() 
//             var chart_cantidades = $("#chart-cantidades").CanvasJSChart()

//             if(data.ordenes_total.length == 0){
//                 $("#chart-error").fadeIn()
//                 panel_reporte.css('display', 'none');
//                 return
//             }

//             $("#chart-error").hide()
//             //Si no, no mostramos error y cargamos los datos en el grafico
//             var ot, ot_vieja
//             for (let i = 0; i < data.ordenes_total.length; i++) {
//                 ot = data["ordenes_total"][i];
//                 ot_vieja = data["ordenes_viejas"][i];

//                 chart_totales.options.data[0].dataPoints.push(
//                     {
//                         label: ot.criterio,
//                         y: parseInt(ot.total),
//                     })
//                 if(ot_vieja){
//                     chart_totales.options.data[1].dataPoints.push(
//                         {
//                             y: parseInt(ot_vieja.total),
//                             label: ot.criterio,
//                         })
//                 }

//                 total_facturado += parseInt(ot.total)
//                 chart_cantidades.options.data[0].dataPoints.push({
//                     label: ot.criterio,
//                     name: ot.criterio,
//                     y: parseInt(ot.cantidad)
//                 })
//             }
//             chart_totales.render()
//             chart_cantidades.render()
//             $("#fecha-ini").html(fecha_ini)
//             $("#fecha-fin").html(fecha_fin)
//             $("#total").html("$" + total_facturado)
//         }})
//         var panel_reporte = $('#reporte_pre').first();
        
//         // Si no lo mostré todavía, mostrarlo.
//         if (panel_reporte.css('display') == 'none') {
//             panel_reporte.css('display', 'inline-block');
//         }
//         // Si está plegado, desplegarlo.
//         if (panel_reporte.find('.x_content').first().css('display', 'none')) {
//             panel_reporte.find('.collapse-link').first().trigger('click');
//         }
// }


$('.chart-input').on('change', function(){
    inicializarGrafico()
  })


$("#btn-ajax").on("click", function(e){
    inicializarGrafico()
})
$("#daterangepicker").on("apply.daterangepicker", function (ev, picker) {

    inicializarGrafico()
    /**
     * Esta es otra forma de manejar el mismo evento que con el callback que se le paso en el constructor
     */

})
function imprimir() {
    var contenido_reporte = {
        titulo: $('#titulo_reporte').text(),
        tiles: [
            {
                tipo: 'grafico',
                titulo: '',
                selector: '#chart-totales',
            },
            {
                tipo: 'html',
                titulo: 'Descripción',
                selector: '#descripcion-cantidades'
            },
            {
                tipo: 'grafico',
                selector: '#chart-cantidades',
            },
        ],
        usuario: '',
    };

    imprimirPDF(contenido_reporte);
}
