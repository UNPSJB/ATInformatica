function randomProperty(obj) {
    var result;
    var count = 0;
    for (var prop in obj)
        if (Math.random() < 1/++count)
           result = prop;
    return result;
}

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
            //Si la lista de ordenes viene vacia, mostramos el error

            // Activar visualizador abajo
            var panel_reporte = $('#reporte_pre').first();

            if(data.ordenes_total.length == 0){
                $("#chart-error").fadeIn()
                panel_reporte.css('display', 'none');
                return
            }

            $("#chart-error").hide()
            //Si no, no mostramos error y cargamos los datos en el grafico
            var total_facturado = 0
            var ot, ot_vieja
            //console.log(data)
            for (let i = 0; i < data.ordenes_total.length; i++) {
                ot = data["ordenes_total"][i];
                ot_vieja = data["ordenes_viejas"][i];

                chartBar.options.data[0].dataPoints.push(
                    {
                        label: ot.criterio,
                        y: parseInt(ot.total),
                    })
                if(ot_vieja){
                    chart.data.datasets[0].data[i] = ot_vieja["total"]
                    chartBar.options.data[1].dataPoints.push(
                        {
                            label: ot.criterio,
                            y: parseInt(ot_vieja.total),
                        })
                }

                total_facturado += parseInt(ot.total)

                chart.data.labels[i] = ot["criterio"]
                chart.data.datasets[1].data[i] = ot["total"]
                cantidad_chart.data.labels.push(ot.criterio)
                cantidad_chart.data.datasets[0].data.push(parseInt(ot.cantidad))
                cantidad_chart.data.datasets[0].backgroundColor.push(COLORES[randomProperty(COLORES)])
            }
            chart.update()
            chartBar.render()
            displayBarLegend(chart, "#chart-total-legend")
            cantidad_chart.update()
            displayDoughnutLegend(cantidad_chart, "#chart-cantidad-legend")
            
            $('#msg-total').show()
            $("#chart-container").show()
            $("#chart-container-cantidad").show()
            $("#fecha-ini").html(fecha_ini)
            $("#fecha-fin").html(fecha_fin)
            $("#total").html("$" + total_facturado)
            $("#total-facturado").show()

            // Si no lo mostré todavía, mostrarlo.
            if (panel_reporte.css('display') == 'none') {
                panel_reporte.css('display', 'inline-block');
            }
            // Si está plegado, desplegarlo.
            if (panel_reporte.find('.x_content').first().css('display', 'none')) {
                panel_reporte.find('.collapse-link').first().trigger('click');                
            }
        },
    });

}

$('.chart-input').on('change', function(){
    inicializarGrafico()
  })


$("#btn-ajax").on("click", function(e){
    inicializarGrafico()
})

function imprimir() {
    
}
