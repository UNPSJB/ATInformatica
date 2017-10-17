// Referencia a la tabla en HTML
var tabla_html = $("#datatable-clientes");

// Serie de atributos para la ventana pop-up
var popup_attrs = "location=no,menubar=no,resizable=no,scrollbars=no";

// Inicializacion y referencia al DataTable, con la config ajax de cada columna
var tabla = tabla_html.DataTable({
    "ajax": tabla_html.attr('data-ajax_url'),   // a qué URL pegarle para obtener los datos
    "columns": [
        {"data": "id",
    "visible": false},  // primera columna oculta: IDs para despues
        {"data": "nombre"},
        {"data": "dni"},
        {"data": "domicilio"},
        {"data": "telefono"},
        {"data": "email"},
        {"data": "saldo"},
    ],
    "dom": "Bfrtip",    
    "buttons": [{
        text: "<b>Nuevo cliente</b>",
        action: function() {
            // TODO: popup crear_cliente y esperar respuesta:
            // pasar la data a parent y cerrar este modal.
            var ventana = window.open(tabla_html.attr('data-popup_url'), 'Crear nuevo cliente', popup_attrs);
        },
        className: "btn-sm btn-info"
    }, ],
});

// Evento: CLICK de una fila, para marcarla como seleccionada agregando la clase "selected"
$('#datatable-clientes tbody').on( 'click', 'tr', function () {
    if ( $(this).hasClass('selected') ) {
        // $(this).removeClass('selected');
        // Comentado para NO deseleccionar :p
    }
    else {
        tabla.$('tr.selected').removeClass('selected');
        $(this).addClass('selected');
        $('#boton_confirmar_cliente').removeClass('disabled');
    }

    // Sanity check: mostrar el ID del cliente clickeado, columna nombrada 'id' por la fuente ajax
    console.log('ID Cliente seleccionado: ' + tabla.row(this).data()['id']);
} );