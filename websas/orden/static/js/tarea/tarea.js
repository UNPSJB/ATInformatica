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
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function aceptarTareas() {

    function getTareas() {
        var ids_tareas = [];
        $('input[name=table_records]:checked').each(function (index, element) {
            ids_tareas.push($(element).attr('data-tarea-id'))
        })
        console.log(ids_tareas)
        return ids_tareas
    }

    data = {
        'tareas': getTareas(),
        'orden_id': $("#tareasPresupuestadas").attr("data-orden-id"),
    }

    console.log(data)

    $.ajax({
        url: $("#tareasPresupuestadas").attr("ajax-url"),
        type: "POST",
        data: data,
        dataType: 'json',
        success: function (res) {
            location.reload();
        }
    })
}

function finalizarTareas() {

    function getTareas() {
        var ids_tareas = [];
        $('input[name=table_records]:checked').each(function (index, element) {
            ids_tareas.push($(element).attr('data-tarea-id'))
        })
        return ids_tareas
    }

    data = {
        'tareas': getTareas(),
        'orden_id': $("#tareasPendientes").attr("data-orden-id"),
    }

    $.ajax({
        url: $("#tareasPendientes").attr("ajax-url"),
        type: "POST",
        data: data,
        dataType: 'json',
        success: function (data) {
            location.reload();
        },
        error: function (data) {
            alert(data.responseJSON.error);
        }
    })
}

function cerrar() {

    data = {
        'orden_id': $("#boton-cerrar").attr("data-orden-id"),
    }

    $.ajax({
        url: $("#boton-cerrar").attr("ajax-url"),
        type: "POST",
        data: data,
        dataType: 'json',
        success: function (data) {
            location.reload();
        },
        error: function (data) {
            alert(data.responseJSON.error);
        }
    })
}


function cancelar() {

    data = {
        'orden_id': $("#boton-cancelar").attr("data-orden-id"),
    }

    $.ajax({
        url: $("#boton-cancelar").attr("ajax-url"),
        type: "POST",
        data: data,
        dataType: 'json',
        success: function (data) {
            location.reload();
        },
        error: function (data) {
            alert(data.responseJSON.error);
        }
    })
}
