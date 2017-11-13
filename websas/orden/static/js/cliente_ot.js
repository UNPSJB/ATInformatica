
var popup
var tabla
$(document).ready(function(){
    get_clientes()
    console.log('tabla_clientes')
})

function close_popup(){
    get_clientes()
    popup.close()
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
            console.log(data)
            $('#clientes').html(data['data'])
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

var tabla_html = $("#datatable-clientes")
var popup_attrs = "location=no,menubar=no,resizable=no,scrollbars=no";


// Inicializacion y referencia al DataTable, con la config ajax de cada columna
function tabla_clientes(){
    tabla_html = $("#datatable-clientes")
    popup_attrs = "location=no,menubar=no,resizable=no,scrollbars=no";

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
    var dtabla = tabla_html.DataTable({
        "responsive": true,
        // "ajax": {'url':'localhost:8000/orden/lista_clientes'},//tabla_html.attr('data-ajax_url'),
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
    return dtabla
}