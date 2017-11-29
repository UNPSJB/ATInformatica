var tabla_html = $("#datatable-rubros");

var botones_default = [{
    extend: "copy",
    text: "Copiar tabla",
    className: "btn-sm"
}, {
    extend: "csv",
    text: "Exportar tabla a CSV",
    className: "btn-sm"
}, {
    extend: "print",
    text: "Imprimir tabla",
    className: "btn-sm"
}];

var botones_dt;

console.log(tabla_html.attr('data-url_agregar'))

if (tabla_html.attr('data-url_agregar')) {
    var boton_agregar = [{
        text: "<b>Nuevo rubro</b>",
        action: function() {
            location.href = tabla_html.attr('data-url_agregar');
        },
        className: "btn-sm btn-info"
    }]

    botones_dt = boton_agregar.concat(botones_default);
} else {
    botones_dt = botones_default;
}

tabla_html.DataTable({
    responsive: true,
    dom: "Bfrtip",
    buttons: botones_dt,
});


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
    console.log(label);
});

$("#daterangepicker").on("apply.daterangepicker", function(ev, picker){

    /**
     * Esta es otra forma de manejar el mismo evento que con el callback que se le paso en el constructor
     */
    console.log("EN EL EVENTO");
    console.log(picker.startDate.format("DD/MM/YYYY"))
    console.log(picker.endDate.format("DD/MM/YYYY"))

    console.log("");
    console.log(Date.parse(picker.startDate));

})