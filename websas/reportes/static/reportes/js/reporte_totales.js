// function randomProperty(obj) {
//     var result;
//     var count = 0;
//     for (var prop in obj)
//         if (Math.random() < 1/++count)
//            result = prop;
//     return result;
// }

//$("#daterangepicker").on("show.daterangepicker", function(ev, picker) {
    /**
     * Evento que se dispara cuando se muestra el datepicker
     */    
    //$("#chart-error").hide()
    //$("#chart-container").hide()
    //$("#chart-container-cantidad").hide()
    //$("#total-facturado").hide()
//})



$("#daterangepicker").on("apply.daterangepicker", function(ev, picker){

    /**
     * Esta es otra forma de manejar el mismo evento que con el callback que se le paso en el constructor
     */

})
$(document).on('ready', function(){
    inicializarGrafico()
})

function inicializarGrafico () {
    //inicializamos graficos
    init_chart()

    var total_facturado = 0
    var picker = $("#daterangepicker").data('daterangepicker')
    var fecha_ini = picker.startDate.format("DD/MM/YYYY")
    var fecha_fin = picker.endDate.format("DD/MM/YYYY")
    var filtro = $("#id_filtros").val()

    $.ajax({
        url: $("form")[0].dataset["ajax_url"],
        type: "GET",
        data: {
            "fecha_ini": fecha_ini,
            "fecha_fin": fecha_fin,
            "filtros": filtro,
        },
        dataType: "json",
        success: function(data){
            console.log(data);
            //Si la lista de ordenes viene vacia, mostramos el error

            // Activar visualizador abajo
            var chart_totales = $("#chart-totales").CanvasJSChart() 
            var chart_cantidades = $("#chart-cantidades").CanvasJSChart()

            if(data.ordenes_total.length == 0){
                $("#chart-error").fadeIn()
                panel_reporte.css('display', 'none');
                return
            }

            $("#chart-error").hide()
            //Si no, no mostramos error y cargamos los datos en el grafico
            var ot, ot_vieja
            //console.log(data)
            for (let i = 0; i < data.ordenes_total.length; i++) {
                ot = data["ordenes_total"][i];
                ot_vieja = data["ordenes_viejas"][i];

                chart_totales.options.data[0].dataPoints.push(
                    {
                        label: ot.criterio,
                        y: parseInt(ot.total),
                    })
                if(ot_vieja){
                    chart_totales.options.data[1].dataPoints.push(
                        {
                            y: parseInt(ot_vieja.total),
                            label: ot.criterio,
                        })
                }

                total_facturado += parseInt(ot.total)
                chart_cantidades.options.data[0].dataPoints.push({
                    label: ot.criterio,
                    name: ot.criterio,
                    y: parseInt(ot.cantidad)
                })
            }
            chart_totales.render()
            chart_cantidades.render()
            $("#fecha-ini").html(fecha_ini)
            $("#fecha-fin").html(fecha_fin)
            $("#total").html("$" + total_facturado)
        }})

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

$('.chart-input').on('change', function(){
    inicializarGrafico()
  })


$("#btn-ajax").on("click", function(e){
    inicializarGrafico()
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
