var popup
var tabla

$(document).ready(function(){
    init_equipos()
});

function init_equipos(){
    var inputrubro = $('input:checked[name=rubro]')[0]
    if (inputrubro){
        var rubro = inputrubro.dataset['idrubro']
        if(rubro){
            get_equipos(rubro)   
        }
        console.log('tabla_clientes')
    }
}

function get_equipos(rubro){

    $.ajax({    
        //la url a donde hay que pegarle en el servidor esta en el html de la tabla
        //de esta forma, podemos tener el .js separado del .html
        url: '/orden/lista_equipos',
        type: "GET",
        dataType: 'json',
        data:{
            'rubro':rubro
        },
        success:function(data){
            console.log(data)
            $('#equipos').html(data['data'])
            $(document).trigger('icheck')
            tabla_equipos()
        }
    })
}

$('#equipo').on('click', function(){
    var equipo_popup = window.open

})


// Inicializacion y referencia al DataTable, con la config ajax de cada columna
function tabla_equipos(){
    var tabla_html = $("#datatable-equipos")
    var popup_attrs = "location=no,menubar=no,resizable=no,scrollbars=no";


    // Inicializacion y referencia al DataTable, con la config ajax de cada columna
    var dtabla = tabla_html.DataTable({
        "responsive": true,
        // "ajax": {'url':'localhost:8000/orden/lista_clientes'},//tabla_html.attr('data-ajax_url'),
        "autoWidth": false,
        "columns": [
            {"data":""},
            {"data": "nro_serie"},
            {"data": "rubro"},
            {"data": "descripcion"},
        ],
        "dom": "Bfrtip",
        "buttons": [{
            text: "<b>Nuevo Equipo</b>",
            action: function() {
                // TODO: si es necesario generar el form de nuevo técnico
                // como modal, este botón puede dispararlo
                // Por ahora sólo pega a crear técnico
                var inputrubro = $('input:checked[name=rubro]')[0]
                var rubro = inputrubro.dataset['idrubro']

                popup = window.open('/orden/equipo/crear_popup/'+parseInt(rubro), 'Agregar nuevo Equipo', popup_attrs);
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

    console.log('dtabla')
    console.log(dtabla)
    return dtabla
}