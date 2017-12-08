function randomProperty(obj) {
    var result;
    var count = 0;
    for (var prop in obj)
        if (Math.random() < 1/++count)
           result = prop;
    return result;
}

$("#daterangepicker").daterangepicker(
{
    startDate: moment().startOf('month'),
    endDate: moment().endOf("month"),
    locale: {
        "format": 'DD/MM/YYYY',
        "applyLabel": "Aceptar",
        "cancelLabel": "Cancelar",
        "fromLabel": "desde",
        "toLabel": "hasta",
        "daysOfWeek": [
            "Dom",
            "Lun",
            "Mar",
            "Mié",
            "Jue",
            "Vie",
            "Sáb"
        ],
        "monthNames": [
            "Enero",
            "Febrero",
            "Marzo",
            "Abril",
            "Mayo",
            "Junio",
            "Julio",
            "Agosto",
            "Septiembre",
            "Octubre",
            "Noviembre",
            "Diciembre"
        ],
    },
    ranges: {
        'Hoy': [moment(), moment()],
        'Ayer': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
        'Este mes': [moment().startOf('month'), moment()],
        'Este trimestre': [moment().subtract(3, "month"), moment()],
        'Desde principio de año': [moment().startOf('month').startOf('year'), moment()],
        'Últimos 7 días': [moment().subtract(6, 'days'), moment()],
        'Últimos 30 días': [moment().subtract(29, 'days'), moment()],
        'Último mes': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')],
        'Último trimestre': [moment().subtract(3, 'month').startOf('month'), moment()],
        'Último año': [moment().subtract(12, 'month'), moment()],
    },
    "alwaysShowCalendars": true,
    "showCustomRangeLabel": false,
    "linkedCalendars": false,

}, 
function(start, end, label){
    /**
     * funcion de callback que se ejecuta cuando se seleccionan fechas validas y se pulsa el boton "Aceptar",
     * o cuando se elige alguno de los rangos predefinidos ("Hoy", "Ayer", "Últimos 7 días", ...)
     */
});
$("#daterangepicker").on("show.daterangepicker", function(ev, picker) {
    /**
     * Evento que se dispara cuando se muestra el datepicker
     */    
    $("#chart-error").hide()
    $("#chart-container").hide()
    $("#chart-container-cantidad").hide()
    $("#total-facturado").hide()
})



$("#daterangepicker").on("apply.daterangepicker", function(ev, picker){

    /**
     * Esta es otra forma de manejar el mismo evento que con el callback que se le paso en el constructor
     */

})

$("#btn-ajax").on("click", function(e){

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
            if(data.ordenes_total.length == 0){
                $("#chart-error .alert").html("<strong>Su consulta no ha generado resultados</strong>")
                $("#chart-error").fadeIn()
                return
            }
            //Si no, no mostramos error y cargamos los datos en el grafico
            var total_facturado = 0
            var ot, ot_vieja
            //console.log(data)
            for (let i = 0; i < data.ordenes_total.length; i++) {
                ot = data.ordenes_total[i];
                ot_vieja = data.ordenes_viejas[i];

                chart.data.labels[i] = ot.criterio
                chart.data.datasets[1].data[i] = ot.total
                if(ot_vieja){
                    chart.data.datasets[0].data[i] = ot_vieja.total
                }

                total_facturado += parseInt(ot.total)

                cantidad_chart.data.labels[i] = ot.criterio
                cantidad_chart.data.datasets[0].data[i] = parseInt(ot.cantidad)
                cantidad_chart.data.datasets[0].backgroundColor[i] = COLORES[randomProperty(COLORES)]
            }
            chart.update()
            displayBarLegend(chart, "#chart-total-legend")
            cantidad_chart.update()
            displayDoughnutLegend(cantidad_chart, "#chart-cantidad-legend")

            $("#chart-container").show()
            $("#chart-container-cantidad").show()
            $("#fecha-ini").html(fecha_ini)
            $("#fecha-fin").html(fecha_fin)
            $("#total").html("$" + total_facturado)
            $("#total-facturado").show()

        },
    })
})

function imprimir(){
    // Init doc
    var doc = new jsPDF({
        orientation: 'p',
        unit: 'mm'
    });

    // Cabecera
    doc.setFontSize(17);
    doc.setFillColor(24,24,24);
    
    doc.rect(4,0,doc.internal.pageSize.width, 25, 'F');

    

    var canvas = $("#chart-ots-clientes")[0];
    var canvasImg = canvas.toDataURL("image/jpg", 0.6);


    var total = 'Total facturado por cliente\nen el período ' + $('#fecha-ini').text() + ' al ' + $('#fecha-fin').text() + ':';
    
    doc.setFontSize(20);
    doc.text(30, 40, total);
    doc.addImage(canvasImg, 'PNG', 30, 80, 70, 70);
    doc.save('prueba.pdf');
}
