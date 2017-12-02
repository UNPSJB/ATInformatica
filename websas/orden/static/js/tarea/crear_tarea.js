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

var tabla_html = $("#datatable-tipo-tarea");

dtabla = tabla_html.DataTable({
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

// Click en la fila para seleccionar
tabla_html.on('click', 'tr', function() {
    var radio = $(this).find('input');
    if (radio[0]) {
        dtabla.$('tr.row_selected').removeClass('row_selected');
        $(this).addClass('row_selected');
        radio.iCheck('checked');
    }
});

function crearTarea(objs, context){
    try {
        $('#error-elem').hide();
        try {
            var data = {
                'tipo_tarea':$('input:checked[name=tipo_tarea]')[0].dataset['idtipotarea'],
                'observacion':$('#observaciontarea').val(),
                'orden_id':$('#id-orden-tarea').text(),
            };
        }
        catch (err) {
            throw "Debe seleccionar una tarea";
        }

        // Pero primero, la observación:
        if (data['observacion'] == '') {
            $('#observaciontarea').select();
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
                403: function(data) {
                    // Mensaje del servidor
                    mostrarError(data.responseJSON.error);
                }
            }
        });
    }
    catch (e) {
        // Mensaje del front
        mostrarError(e);
    }
}

function mostrarError(mensaje) {
    $('#errormsg').html(mensaje);
    $('#error-elem').fadeIn();
}

$('#modalTarea').on('hidden.bs.modal', function () {
    location.reload()
});

// $("input:checked[name=tipo_tarea]:radio").change(function () {
//     console.log("ea")
//     // alert(this.value)
// })