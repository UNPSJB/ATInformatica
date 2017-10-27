// Inicializacion Smart Wizard
$(document).ready(function(){
    get_clientes()   
    tabla_clientes()


})

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

$('#creacion_ot').smartWizard({
    labelNext:'Siguiente',
    labelPrevious:'Anterior',
    labelFinish:'Finalizar',
    onLeaveStep: function(obj, context){
        console.log("Leaving step " + context.fromStep + " to go to step " + context.toStep);
        return true;
    },
    onFinish: crearOrden
});


// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');



function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function crearOrden(objs, context){
    var data = {
        'cliente':$('input:checked[name=cliente]')[0].dataset['idcliente'],
        'tecnico':$('input:checked[name=tecnico]')[0].dataset['idtecnico'],
        'servicio':$('input:checked[name=tipo_servicio]')[0].dataset['idtiposervicio'],
        'rubro':$('input:checked[name=rubro]')[0].dataset['idrubro']
    }

    console.log(data)
    $.ajax({    
        //la url a donde hay que pegarle en el servidor esta en el html de la tabla
        //de esta forma, podemos tener el .js separado del .html
        url: $("#creacion_ot").attr("ajax-url"),
        type: "POST",
        data: data,
        dataType: 'json',
        success: function(data){
            console.log("en la success function");
            console.log(data)
        }
    })
}

$('#agregar_cliente').on('click', function(){
    var cliente_popup = window.open

})
function listado_clientes(clientes){
    console.log(clientes)

}

function tabla_clientes(){
    var tabla_html = $("#datatable-clientes")
    var popup_attrs = "location=no,menubar=no,resizable=no,scrollbars=no";


    // Inicializacion y referencia al DataTable, con la config ajax de cada columna
    var tabla = tabla_html.DataTable({
        "responsive": true,
        "ajax": {'url':'localhost:8000/orden/lista_clientes'},//tabla_html.attr('data-ajax_url'),
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
                var ventana = window.open(tabla_html.attr('data-popup_url'), 'Crear nuevo cliente', popup_attrs);
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
}