// Referencia a la tabla en HTML
var tabla_html = $("#datatable-clientes")

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
        text: "<b>Nuevo cliente</b>",
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

$(function() {
    $('#contenido_cargando').attr('hidden', true);
    $('#contenido_tabla').attr('hidden', false);
});
