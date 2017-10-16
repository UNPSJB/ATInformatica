var tabla = $("#datatable-clientes").DataTable({
    responsive: true,
    select: true,
    buttons: [{
        text: "<b>Nuevo cliente</b>",
        action: function() {
            // TODO: POPUP-CREACION
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