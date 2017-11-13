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


$("#datatable-tipo-tarea").DataTable({
    responsive: true,
    dom: "Bfrtip",
    buttons: [{
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

function crearTarea(objs, context){
    try {
        try {
            var data = {
                'tipo_tarea':$('input:checked[name=tipo_tarea]')[0].dataset['idtipotarea'],
                'observacion':$('#observaciontarea').val(),
                'estado_orden':$('#id-orden-tarea').text(),
            };
        }
        catch (err) {
            throw "Debe seleccionar una tarea";
        }
        
        if (data['observacion'] == '') {
            throw "No puede dejar la observación en blanco";
        }

    
        $.ajax({    
            url: $("#crearTarea").attr("ajax-url"),
            type: "POST",
            data: data,
            dataType: 'json',
            success: function(data){
                $('#modalTarea').modal('toggle');    
            },
            statusCode: {
                500: manejador_500(data)
                }
            });

        function manejador_500(e) {
            throw "La tarea seleccionada ya fue agregada a la Orden de Trabajo";
        };
    }

    catch (e) {
        $('#errormsg').html(e);
        $('#error-elem').fadeIn();
    }
}

$('#modalTarea').on('hidden.bs.modal', function () {
    location.reload()
});


