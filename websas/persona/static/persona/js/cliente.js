// Referencia a la tabla en HTML
var tabla_html = $("#datatable-clientes")

// Inicializacion y referencia al DataTable, con la config ajax de cada columna
var tabla = tabla_html.DataTable({
    "responsive": true,
    "ajax": tabla_html.attr('data-ajax_url'),
    "columns": [
        {"data": "id",
        "visible": false},
        {"data": "nombre"},
        {"data": "dni"},
        {"data": "domicilio"},
        {"data": "telefono"},
        {"data": "email"},
        {"data": "saldo"},
        {"data": "url_ver", "render": function(url) {
            return '<a href="'+ url + '"><i class="fa fa-eye"></i></a>';
        }},
        {"data": "url_editar", "render": function(url) {
            return '<a href="'+ url + '"><i class="fa fa-pencil"></i></a>';
        }},
        {"data": "url_eliminar", "render": function(url) {
            return '<a href="'+ url + '"><i class="fa fa-trash"></i></a>';
        }},
    ],
    "dom": "Bfrtip",
    "buttons": [{
        text: "<b>Nuevo cliente</b>",
        action: function() {
            // TODO: si es necesario generar el form de nuevo técnico
            // como modal, este botón puede dispararlo
            // Por ahora sólo pega a crear técnico
            location.href = "/cliente/crear";
        },
        className: "btn-sm btn-info"
    }, {
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
    }, ],
});


$('#datatable-clientes tbody').on('click', 'tr', function() {
    var datosFila = tabla.row(this).data();
    // console.log("AHRE")
    console.log('Data: ' + datosFila);
});

