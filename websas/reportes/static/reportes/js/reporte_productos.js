$(document).ready(function(){
    inicializarGrafico()
})

$("#check-filtrarencero").on('change', function() {
    inicializarGrafico();
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
    var criterio = $("form").find("select option:selected").text();
    $('.criterio').text(criterio.toLowerCase());
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
        opcionesGrafico: {
            filtrar_en_cero: $('#check-filtrarencero').is(':checked'),
        }
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
    var chart_cantidades = $("#chart-cantidades").CanvasJSChart();
    var total_facturado = 0
    var total_facturado_productos = 0

    // Info de las tablas de datos
    var info_tabla = [];
    var info_tabla_cantidades = [];
    
    
    // Recorrido de facturado en las dos series de datos (total facturado y productos facturados) - según criterio
    for (let i = 0; i < chart_totales.options.data[0].dataPoints.length; i++) {
        const element = chart_totales.options.data[0].dataPoints[i];
        var valor = parseFloat(element["y"]);
        var valor_productos = 0;
        if (valor > 0) {
            // Sumar total facturado
            total_facturado += valor;

            // Si tengo un valor para productos, lo busco y proceso
            // Usar .find para matchear por element.name contra name
            var match = chart_totales.options.data[1].dataPoints.find(x => x.name == element.name);
            if (match != undefined) {
                valor_productos = parseFloat(match["y"]);
                total_facturado_productos += valor_productos;
            }

            info_tabla.push({
                'nombre': element.name,
                'total_facturado': valor,
                'parte_productos': valor_productos,
                'porcentaje': valor_productos / valor * 100,
            });
        }
    }

    info_tabla.sort(function(a, b) {
        if (a['parte_productos'] > b['parte_productos']) {
            return -1;
        } else if (a['parte_productos'] < b['parte_productos']) {
            return 1;
        }
        return 0;
    });

    var tabla_datos_body = $('#tabla-totales').find('tbody').first();
    $('#tabla-totales tr.datos').remove();

    // Un for para mostrar no más de 5 registros del array ordenado
    for (var i = 0; i<Math.min(info_tabla.length, 5); i++) {
        e = info_tabla[i];
        var fila = '<tr class="datos"><td>' + e.nombre + '</td><td>$ ' + e.total_facturado.toLocaleString('es-AR', {minimumFractionDigits: 2, maximumFractionDigits: 2}) + '</td><td>$ ' + e.parte_productos.toLocaleString('es-AR', {minimumFractionDigits: 2, maximumFractionDigits: 2}) + '</td><td>' + e.porcentaje.toLocaleString('es-AR', {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' %</td></tr>';
        tabla_datos_body.append(fila);
    };

    $("#total").html("$ " + total_facturado.toLocaleString('es-AR', {minimumFractionDigits: 2, maximumFractionDigits: 2}));
    $("#total-productos").html("$ " + total_facturado_productos.toLocaleString('es-AR', {minimumFractionDigits: 2, maximumFractionDigits: 2}));


    // Recorrido de las cantidades para armar la tabla de datos
    for (let i = 0; i < chart_cantidades.options.data[0].dataPoints.length; i++) {
        const element = chart_cantidades.options.data[0].dataPoints[i];
        var valor = parseInt(element["y"]);
        if (valor > 0) {
            info_tabla_cantidades.push({
                'nombre': element.name,
                'cantidad': valor,
            });
        }
    }

    info_tabla_cantidades.sort(function(a, b) {
        if (a['cantidad'] > b['cantidad']) {
            return -1;
        } else if (a['cantidad'] < b['cantidad']) {
            return 1;
        }
        return 0;
    });

    var tabla_datos_cant_body = $('#tabla-cantidades').find('tbody').first();
    $('#tabla-cantidades tr.datos').remove();

    // Un for para mostrar no más de 5 registros del array ordenado
    for (var i = 0; i<Math.min(info_tabla_cantidades.length, 5); i++) {
        e = info_tabla_cantidades[i];
        var fila = '<tr class="datos"><td>' + e.nombre + '</td><td>' + e.cantidad + '</td></tr>';
        tabla_datos_cant_body.append(fila);
    };

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
    });

    $('#td-totalfacturado').text('$ ' + total_facturado.toLocaleString('es-AR', {minimumFractionDigits: 2, maximumFractionDigits: 2}));
    $('#td-totalfacturadoproductos').text('$ ' + total_facturado_productos.toLocaleString('es-AR', {minimumFractionDigits: 2, maximumFractionDigits: 2}));
    $('#td-manodeobra').text('$ ' + (total_facturado - total_facturado_productos).toLocaleString('es-AR', {minimumFractionDigits: 2, maximumFractionDigits: 2}));
    var porcentaje_productos = total_facturado_productos / total_facturado * 100
    $('#td-porcentajeproductos').text(porcentaje_productos.toLocaleString('es-AR', {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' %');
}

function imprimir() {
    var contenido_reporte = {
        titulo: $('#titulo-reporte').text(),
        nombre_archivo: "Reporte_productos_" + moment().format("DD/MM/YYYY") + ".pdf",
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
                tipo: 'div',
                selector: '#titulo_reporte',
                ancho: true,
            },
            {
                tipo: 'grafico',
                selector: '#chart-totales-productos',
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
            {
                tipo: 'hr'
            },
            {
                tipo: 'div',
                selector: '#div-tabla-3',
            },
            {
                tipo: 'grafico',
                selector: '#chart-porcentajes',
            },
        ],
        usuario: get_nombreusuario(),
    };

    imprimirPDF(contenido_reporte);}
