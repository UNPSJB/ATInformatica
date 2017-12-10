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
