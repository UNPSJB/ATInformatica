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
    if (data.tareas.length > 0) {
        $.ajax({
            url: $("#tareasPresupuestadas").attr("ajax-url"),
            type: "POST",
            data: data,
            dataType: 'json',
            success: function (res) {
                location.reload();
            },
            error: function (data) {
                modalError("Error en la operación", "El servidor no pudo procesar la solicitud", data.responseJSON.error);
            }
        });
    }
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

    if (data.tareas.length > 0) {
        $.ajax({
            url: $("#tareasPendientes").attr("ajax-url"),
            type: "POST",
            data: data,
            dataType: 'json',
            success: function (data) {
                location.reload();
            },
            error: function (data) {
                modalError("Error en la operación", "El servidor no pudo procesar la solicitud", data.responseJSON.error);
            }
        });
    }
}

function modalError(titulo, subtitulo, texto) {
    {
        $('.modal').each(function(index, element) {
            $(element).hide();
        });
    }
    var modal_html = $('#modal-error');
    var modal_titulo = $('#modal-error-titulo');
    var modal_subtitulo = $('#modal-error-subtitulo');
    var modal_texto = $('#modal-error-texto');

    modal_titulo.html(titulo);
    modal_subtitulo.html(subtitulo);
    modal_texto.html(texto);

    modal_html.modal();
}

function cerrar() {

    data = {
        'orden_id': $("#boton-cerrar").attr("data-orden-id"),
    }

    // TODO: mostrar confirmación si tareas pendientes

    $.ajax({
        url: $("#boton-cerrar").attr("ajax-url"),
        type: "POST",
        data: data,
        dataType: 'json',
        success: function (data) {
            location.reload();
        },
        error: function (data) {
            modalError("Error en la operación", "El servidor no pudo procesar la solicitud", data.responseJSON.error);
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
            location.assign($('#btn-volver-listado').attr('href'));
        },
        error: function (data) {
            modalError("Error en la operación", "El servidor no pudo procesar la solicitud", data.responseJSON.error);
        }
    })
}



// Table
$('table input').on('ifChecked', function() {
    checkState = '';
    $(this).parent().parent().parent().addClass('selected');
    countChecked();
});
$('table input').on('ifUnchecked', function() {
    checkState = '';
    $(this).parent().parent().parent().removeClass('selected');
    countChecked();
});

var checkState = '';

$('.bulk_action input').on('ifChecked', function() {
    checkState = '';
    $(this).parent().parent().parent().addClass('selected');
    countChecked();
});
$('.bulk_action input').on('ifUnchecked', function() {
    checkState = '';
    $(this).parent().parent().parent().removeClass('selected');
    countChecked();
});
$('.bulk_action input#check-all').on('ifChecked', function() {
    checkState = 'all';
    countChecked();
});
$('.bulk_action input#check-all').on('ifUnchecked', function() {
    checkState = 'none';
    countChecked();
});

function countChecked() {
    if (checkState === 'all') {
        $(".bulk_action input[name='table_records']").iCheck('check');
    }
    if (checkState === 'none') {
        $(".bulk_action input[name='table_records']").iCheck('uncheck');
    }

    var checkCount = $(".bulk_action input[name='table_records']:checked").length;

    if (checkCount) {
        $('.column-title').hide();
        $('.bulk-actions').show();
        $('.action-cnt').html(checkCount + ' Records Selected');
    } else {
        $('.column-title').show();
        $('.bulk-actions').hide();
    }
}
