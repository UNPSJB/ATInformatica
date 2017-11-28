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

$(function () {

    var start = moment().subtract(29, 'days');
    var end = moment();

    function cb(start, end) {
        $('#reportrange span').html(start.format('DD/MM/YYYY') + ' - ' + end.format('DD/MM/YY'));
    }

    $("input[name='daterangepicker']").daterangepicker({
        startDate: start,
        endDate: end,
        locale: {
            format: 'DD/MM/YYYY'
        },
        ranges: {
            'Today': [moment(), moment()],
            'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
            'Last 7 Days': [moment().subtract(6, 'days'), moment()],
            'Last 30 Days': [moment().subtract(29, 'days'), moment()],
            'This Month': [moment().startOf('month'), moment().endOf('month')],
            'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
        },
        "alwaysShowCalendars": true,
    }, cb);

    cb(start, end);

});


// $("input[name='daterangepicker']").daterangepicker({
//     "dateLimit": {
//         "days": 7
//     },
//     "ranges": {
//         "Today": [
//             "2017-11-28T20:17:46.341Z",
//             "2017-11-28T20:17:46.341Z"
//         ],
//         "Yesterday": [
//             "2017-11-27T20:17:46.341Z",
//             "2017-11-27T20:17:46.341Z"
//         ],
//         "Last 7 Days": [
//             "2017-11-22T20:17:46.341Z",
//             "2017-11-28T20:17:46.341Z"
//         ],
//         "Last 30 Days": [
//             "2017-10-30T20:17:46.341Z",
//             "2017-11-28T20:17:46.341Z"
//         ],
//         "This Month": [
//             "2017-11-01T03:00:00.000Z",
//             "2017-12-01T02:59:59.999Z"
//         ],
//         "Last Month": [
//             "2017-10-01T03:00:00.000Z",
//             "2017-11-01T02:59:59.999Z"
//         ]
//     },
//     "alwaysShowCalendars": true,
//     "startDate": "11/22/2017",
//     "endDate": "11/28/2017",
//     "opens": "center"
// }, function (start, end, label) {
//     console.log("New date range selected: ' + start.format('YYYY-MM-DD') + ' to ' + end.format('YYYY-MM-DD') + ' (predefined range: ' + label + ')");
// });


// $("input[name='daterangepicker']").daterangepicker(
//     {
//         locale: {
//             format: 'DD/MM/YYYY'
//         },
//         startDate: '01/01/2017',
//         endDate: '31/12/2017'
//     }
// )