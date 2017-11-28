var popup
var tabla
var dtabla

$(document).ready(function() {
    get_clientes()
    console.log('tabla_clientes')
})

function close_popup(){
    popup.close()
    get_clientes()
}

function get_clientes(){

    console.log('update clientes')
    $.ajax({    
        //la url a donde hay que pegarle en el servidor esta en el html de la tabla
        //de esta forma, podemos tener el .js separado del .html
        url: '/orden/lista_clientes',
        type: "GET",
        dataType: 'json',
        success:function(data){
            console.log('clientes=success')
            console.log(data)
            $('#clientes').html(data['data'])
            $(document).trigger('icheck')
            tabla_clientes()
        }
    })
}

$('#agregar_cliente').on('click', function(){
    var cliente_popup = window.open

})
function listado_clientes(clientes){
    console.log(clientes)

}

// Inicializacion y referencia al DataTable, con la config ajax de cada columna
function tabla_clientes(){
    var tabla_html = $("#datatable-clientes")
    var popup_attrs = "location=no,menubar=no,resizable=no,scrollbars=no";

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
    
    console.log(tabla_html.attr('data-popup_url'))
    
    if (tabla_html.attr('data-popup_url')) {
        var boton_agregar = [{
            text: "<b>Nuevo cliente</b>",
            action: function() {
                popup = window.open(tabla_html.attr('data-popup_url'), 'Crear nuevo cliente', popup_attrs);
            },
            className: "btn-sm btn-info"
        }]
    
        botones_dt = boton_agregar.concat(botones_default);
    } else {
        botones_dt = botones_default;
    }

    // Inicializacion y referencia al DataTable, con la config ajax de cada columna
    dtabla = tabla_html.DataTable({
        // "ajax": {'url':'localhost:8000/orden/lista_clientes'},//tabla_html.attr('data-ajax_url'),
        "autoWidth": false,
        "columns": [
            {"data":"radio"},
            {"data": "nombre"},
            {"data": "dni"},
            {"data": "domicilio"},
            {"data": "telefono"},
            {"data": "email"},
        ],
        "dom": "Bfrtip",
        "buttons": botones_dt
    });

    console.log('dtabla')
    console.log(dtabla)
    $('#cargando').fadeOut();
    tabla_html.fadeIn();
    $('#creacion_ot').smartWizard('fixHeight');

    // Click en la fila para seleccionar
    tabla_html.on('click', 'tr', function() {
        var radio = $(this).find('input');
        if (radio[0]) {
            dtabla.$('tr.row_selected').removeClass('row_selected');
            $(this).addClass('row_selected');
            radio.iCheck('checked');
        }
    });

    return dtabla
}