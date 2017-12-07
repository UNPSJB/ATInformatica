$("#daterangepicker").daterangepicker(
{
    startDate: moment().subtract(29, 'days'),
    endDate: moment(),
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
        'Últimos 7 días': [moment().subtract(6, 'days'), moment()],
        'Últimos 30 días': [moment().subtract(29, 'days'), moment()],
        'Este mes': [moment().startOf('month'), moment().endOf('month')],
        'Último mes': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')],
        'Último trimestre': [moment().subtract(3, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
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
    console.log("NUEVA FECHA: " + start.format("DD-MM-YYYY") + " a " + end.format("DD-MM-YYYY"))
});
$("#daterangepicker").on("show.daterangepicker", function(ev, picker) {
    /**
     * Evento que se dispara cuando se muestra el datepicker
     */    
    $("#chart-error").hide()
    $("#chart-container").hide()
    $("#total-facturado").hide()
})



$("#daterangepicker").on("apply.daterangepicker", function(ev, picker){

    /**
     * Esta es otra forma de manejar el mismo evento que con el callback que se le paso en el constructor
     */

    init_chart()

    var fecha_ini = picker.startDate.format("DD/MM/YYYY")
    var fecha_fin = picker.endDate.format("DD/MM/YYYY")

    $.ajax({
        url: $(location).attr("href"),
        type: "GET",
        data: {
            "fecha_ini": fecha_ini,
            "fecha_fin": fecha_fin,
        },
        dataType: "json",
        success: function(data){
            //Si la lista de ordenes viene vacia, mostramos el error
            if(data.ordenes_total.length == 0){
                //$("#chart-error").addClass("alert-warning")                
                $("#chart-error").html("<strong>Su consulta no ha generado resultados</strong>")
                $("#chart-error").fadeIn()
                return
            }
            //Si no, no mostramos error y cargamos los datos en el grafico
            var total_facturado = 0
            for (let i = 0; i < data.ordenes_total.length; i++) {
                const ot = data.ordenes_total[i];
                chart.data.labels.push(ot.propietario)
                chart.data.datasets[0].data.push(ot.total)
                total_facturado += parseInt(ot.total)
            }
            chart.update()
            //mostramos el grafico
            $("#chart-container").show()
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
