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

    var criterio_reporte = $("#id_filtros option:selected").text();

    $("#chart-totales").reporteSAS({
        opcionesDataset: [
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
        ],
        opcionesGrafico: {
            titulo: "Facturado en el año actual y el anterior por " + criterio_reporte,
            filtrar_en_cero: $('#check-filtrarencero').is(':checked'),
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
            titulo: "Cantidad de órdenes de trabajo por " + criterio_reporte,
            filtrar_en_cero: $('#check-filtrarencero').is(':checked'),
        }
    });

    // Seleccionar gráficos para recuperar algunos datos
    var chart_totales = $("#chart-totales").CanvasJSChart();
    var chart_cantidades = $("#chart-cantidades").CanvasJSChart();
    
    var total_facturado = 0

    // Info de las tablas de datos
    var info_tabla = [];
    var info_tabla_cantidades = [];

    // Recorrer el dataset del gráfico de facturado por criterio para ir sumando los precios totales de las OTs
    // y a la vez armar la tabla de datos.
    for (let i = 0; i < chart_totales.options.data[1].dataPoints.length; i++) {
        const element = chart_totales.options.data[1].dataPoints[i];
        var valor = parseFloat(element["y"]);
        if (valor > 0) {
            // Sumar al total facturado en este periodo
            total_facturado += valor;

            // Si hay info de facturación del año anterior, recuperar el valor
            if (chart_totales.options.data[0].dataPoints[i])
                valor_anterior = parseFloat(chart_totales.options.data[0].dataPoints[i].y);
            else
                valor_anterior = 0;

            // Agregar al array de elementos de la tabla para mostrar
            info_tabla.push({
                'nombre': element.name,
                'valor': valor,
                'anterior': valor_anterior,  // Valor del año pasado
                'diff': valor - valor_anterior
            });

            info_tabla.sort(function(a, b) {
                if (a['valor'] > b['valor']) {
                    return -1;
                } else if (a['valor'] < b['valor']) {
                    return 1;
                }
                return 0;
            });
        }
    }

    // Actualizar la tabla de datos de facturación (macumba HTML)
    var tabla_datos_body = $('#tabla-totales').find('tbody').first();
    $('#tabla-totales tr.datos').remove();

    // Un for para mostrar no más de 5 registros del array ordenado
    for (var i = 0; i<Math.min(info_tabla.length, 5); i++) {
        e = info_tabla[i];
        var fila = '<tr class="datos"><td>' + e.nombre + '</td><td>$ ' + e.anterior.toLocaleString('es-AR', {minimumFractionDigits: 2}) + '</td><td>$ ' + e.valor.toLocaleString('es-AR', {minimumFractionDigits: 2}) + '</td><td>$ ' + e.diff.toLocaleString('es-AR', {minimumFractionDigits: 2}) + '</td></tr>';
        tabla_datos_body.append(fila);
    };

    // ~~ GRAFICO CANTIDADES ~~

    // Recorrer el dataset del gráfico de cantidades para armar la tabla de datos.
    for (let i = 0; i < chart_cantidades.options.data[0].dataPoints.length; i++) {
        const element = chart_cantidades.options.data[0].dataPoints[i];
        var valor = parseInt(element["y"]);
        if (valor > 0) {
            // Agregar al array de elementos de la tabla para mostrar
            info_tabla_cantidades.push({
                'nombre': element.name,
                'cantidad': valor,
            });

            // Ordenar con función de comparación innecesariamente explícita
            info_tabla_cantidades.sort(function(a, b) {
                if (a['cantidad'] > b['cantidad']) {
                    return -1;
                } else if (a['cantidad'] < b['cantidad']) {
                    return 1;
                }
                return 0;
            });
        }
    }

    // Actualizar la tabla de datos de facturación (macumba HTML)
    var tabla_datos_cant_body = $('#tabla-cantidades').find('tbody').first();
    $('#tabla-cantidades tr.datos').remove();

    // Nuevamente, mostrar no más de 5 registros
    for (var i = 0; i<Math.min(info_tabla_cantidades.length, 5); i++) {
        e = info_tabla_cantidades[i];
        var fila = '<tr class="datos"><td>' + e.nombre + '</td><td>' + e.cantidad + '</td></tr>';
        tabla_datos_cant_body.append(fila);
    };

    $("#total").html("$ " + total_facturado.toLocaleString('es-AR', {minimumFractionDigits: 2}))



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
                tipo: 'div',
                selector: '#descripcion-reporte',
                ancho: true,
            },
            {
                tipo: 'hr',
            },
            {
                tipo: 'grafico',
                selector: '#chart-totales',
                ancho: true,
            },
            {
                tipo: 'div',
                selector: '#div-tabla-1',
                ancho: true,
            },
            {
                tipo: 'hr',
            },
            {
                tipo: 'grafico',
                selector: '#chart-cantidades',
            },
            {
                tipo: 'div',
                selector: '#div-tabla-2',
            },
        ],
        usuario: get_nombreusuario(),
    };

    imprimirPDF(contenido_reporte);
}
