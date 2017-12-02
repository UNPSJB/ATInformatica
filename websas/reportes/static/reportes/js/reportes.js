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
        'Último mes': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
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
    $("#ahre").hide()
    
})



$("#daterangepicker").on("apply.daterangepicker", function(ev, picker){

    /**
     * Esta es otra forma de manejar el mismo evento que con el callback que se le paso en el constructor
     */

    init_chart()

    $.ajax({
        url: $(location).attr("href"),
        type: "POST",
        data: {
            "fecha_ini": picker.startDate.format("DD/MM/YYYY"),
            "fecha_fin": picker.endDate.format("DD/MM/YYYY"),
        },
        dataType: "json",
        success: function(data){
            $("#chart-container").show()
            for (let i = 0; i < data.ordenes.length; i++) {
                const ot = data.ordenes[i];
                chart.data.labels.push(ot.propietario)
                chart.data.datasets[0].data.push(ot.total)
                chart.update()
                console.log(ot.propietario, ot.total);
            }
        },
    })
})

