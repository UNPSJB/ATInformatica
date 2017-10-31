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


function crearTarea(objs, context){
    var data = {
        'tipo_tarea':$('input:checked[name=tipo_tarea]')[0].dataset['idtipotarea'],
        'observacion':$('#observaciontarea').val(),
        'estado_orden':$('#id-orden-tarea').text(),
    }

    console.log(data)
    $.ajax({    
        url: $("#crearTarea").attr("ajax-url"),
        type: "POST",
        data: data,
        dataType: 'json',
        success: function(data){
            console.log("en la success function");
            console.log(data)
            $('#modalTarea').modal('toggle');    
        }
    })
}

$('#modalTarea').on('hidden.bs.modal', function () {
    console.log('Fired when hide event has finished!');
    location.reload()
});