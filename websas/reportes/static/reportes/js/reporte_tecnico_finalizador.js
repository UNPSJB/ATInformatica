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

    $("#fecha-ini").html(fecha_ini.format("DD/MM/YYYY"))
    $("#fecha-fin").html(fecha_fin.format("DD/MM/YYYY"))
    var tipo_tarea = $("form").find("#form-tipo_tarea select option:selected")
    var tipo_servicio = $("form").find("#form-tipo-servicio select option:selected")
    
    console.log(tipo_tarea.text());
    
    $("#span-tipo_tarea").html(tipo_tarea.text())
    $("#span-tipo-servicio").html(tipo_servicio.text())
    
    var chart = $("#chart-tecnico-finalizador").reporteSAS({
        opcionesDataset: [
            {
                tipochart: 'column',
                x: 'tecnico',
                y: 'cantidad',
                dataset: "tecnico_finalizador",
                textoLeyenda: "Cantidad de tareas realizadas por técnico",
                opcionesAjax: {
                    fecha_ini: fecha_ini.format("DD/MM/YYYY"),
                    fecha_fin: fecha_fin.format("DD/MM/YYYY"),
                    tipo_tarea: tipo_tarea.val(),
                    tipo_servicio: tipo_servicio.val(),
                    ajaxurl: $("form")[0].dataset["ajax_url"],
                },
            },
            // /**
            //  * YA FEU NO SE COMPARA NADA
            //  */
            // {
            //     tipochart: 'column',
            //     x: 'tipo_tarea',
            //     y: 'cant',
            //     dataset: "tarea_mas_realizada",
            //     textoLeyenda: "Resumen del año anterior",
            //     opcionesAjax: {
            //         fecha_ini: fecha_ini_vieja.format("DD/MM/YYYY"),
            //         fecha_fin: fecha_fin_vieja.format("DD/MM/YYYY"),
            //         rubro: rubro.val(),
            //         tipo_servicio: tipo_servicio.val(),
            //         ajaxurl: $("form")[0].dataset["ajax_url"],
            //     },
            // },
        ],
        opcionesGrafico: {
            nombre_eje_y: "Cantidad de tareas realizadas",
            nombre_eje_x: "Técnicos",
            intervalo_eje_y: 1,
        }
    });

    var chart_totales = $('#chart-tecnico-finalizador').CanvasJSChart();
    var info_tabla = [];
    try {
        chart_totales.options.data[0].dataPoints.forEach(function(e) {
            info_tabla.push({
                'nombre_tecnico': e.name,
                'cantidad': e.y,
            });
        });
    } catch(e) {

    }

    info_tabla.sort(function(a, b) {
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
    for (var i = 0; i<Math.min(info_tabla.length, 15); i++) {
        e = info_tabla[i];
        var fila = '<tr class="datos"><td>' + e.nombre_tecnico + '</td><td>' + e.cantidad + '</td></tr>';
        tabla_datos_cant_body.append(fila);
    };

    // $("#chart-cantidades").reporteSAS({
    //     opcionesDataset: [
    //         {
    //             tipochart: 'doughnut',
    //             x: 'criterio',
    //             y: 'cantidad',
    //             dataset: "cantidad_productos",
    //             // textoLeyenda: "Facturado en el año actual",
    //             opcionesAjax: {
    //                 fecha_ini: fecha_ini.format("DD/MM/YYYY"),
    //                 fecha_fin: fecha_fin.format("DD/MM/YYYY"),
    //                 filtro: $("#id_filtros").val(),
    //                 ajaxurl: $("form")[0].dataset["ajax_url_cantidad"],
    //             },
    //         },
    //     ],
    //     opcionesGrafico: {}
    // });


//     var chart_totales = $("#chart-totales-productos").CanvasJSChart()
//     var total_facturado = 0
//     var total_facturado_productos = 0
//     for (let i = 0; i < chart_totales.options.data[0].dataPoints.length; i++) {
//         const element = chart_totales.options.data[0].dataPoints[i];
//         total_facturado += parseInt(element["y"])
//     }
    
//     $("#total").html("$ " + total_facturado)

//     for (let i = 0; i < chart_totales.options.data[1].dataPoints.length; i++) {
//         const element = chart_totales.options.data[1].dataPoints[i];
//         total_facturado_productos += parseInt(element["y"])
//     }
//     $("#total-productos").html("$ " + total_facturado_productos)
//     $("#chart-porcentajes").CanvasJSChart({
        
//         data: [
//             {
//                 type: "doughnut",
//                 showInLegend: true,
//                 dataPoints: [
//                     { label: "Mano de obra", name: "Mano de obra", y: total_facturado },
//                     { label: "Productos", name: "Productos", y: total_facturado_productos },
//                 ],
//             },
//         ],
//     })
}

function imprimir() {
    var contenido_reporte = {
        titulo: $('#titulo-reporte').text(),
        nombre_archivo: "Reporte_tecnico_finalizador_" + moment().format("DD/MM/YYYY") + ".pdf",
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
                selector: '#div-grafico-1',
                ancho: true,
            },
            {
                tipo: 'div',
                selector: '#div-tabla-1',
                ancho: true,
            },
        ],
        usuario: get_nombreusuario(),
    };

    imprimirPDF(contenido_reporte);
}
