var tabla = $("#datatable-clientes");
var popup_attrs = "menubar=no,resizable=no,scrollbars=no";

tabla.DataTable({
    responsive: true,
    dom: "Bfrtip",    
    buttons: [{
        text: "<b>Nuevo cliente</b>",
        action: function() {
            // TODO: popup crear_cliente y esperar respuesta:
            // pasar la data a parent y cerrar este modal.
            var ventana = window.open(tabla.attr('data-popup_url'), 'Crear nuevo cliente', popup_attrs);
        },
        className: "btn-sm btn-info"
    }, ],
});

$('#datatable-clientes tbody').on( 'click', 'tr', function () {
    if ( $(this).hasClass('selected') ) {
        $(this).removeClass('selected');
    }
    else {
        tabla.$('tr.selected').removeClass('selected');
        $(this).addClass('selected');
    }
    console.log('ID Cliente seleccionado: ' + $(this).attr('data-idcliente'));
} );