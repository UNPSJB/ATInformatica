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
        $('#error-elem').hide();
        try {
            // var precio_coma = $('#precio-tarea').val().replace(',', '.')

            var data = {
                'tipo_tarea':$('input:checked[name=tipo_tarea]')[0].dataset['idtipotarea'],
                'observacion':$('#observaciontarea').val(),
                // 'precio':parseFloat(precio_coma),
                'orden_id':$('#id-orden-tarea').text(),
            };
        }
        catch (err) {
            throw "Debe seleccionar una tarea";
        }

        // // Precio parseado... a ver qué tenemos: inválido || negativo?
        // if (isNaN(data['precio']) || data['precio'] < 0) {
        //     $('#precio-tarea').select();
        //     throw "El precio ingresado no es válido";
        // }
        // // Precio OK, luego comparamos si hubo que reemplazar coma por punto
        // // Pero primero, la observación:
        // if (data['observacion'] == '') {
        //     $('#observaciontarea').select();
        //     throw "No puede dejar la observación en blanco";
        // }
        // // Reemplazar el campo precio con lo parseado si es necesario
        // if ($('#precio-tarea').val() != data['precio'].toString()) {
        //     $('#precio-tarea').val(data['precio'].toString());
        //     $('#precio-tarea').select();
        //     throw '<span class="text-info">Confirme el precio ingresado y presione "Guardar" nuevamente</span>';
        // }

        $.ajax({    
            url: $("#crearTarea").attr("ajax-url"),
            type: "POST",
            data: data,
            dataType: 'json',
            success: function(data){
                $('#modalTarea').modal('toggle');    
            },
            statusCode: {
                500: function(data) {
                    throw "La tarea seleccionada ya fue agregada a la Orden de Trabajo";
                },
                403: function(data) {
                    console.log(data);
                }
            }
        });
    }
    catch (e) {
        $('#errormsg').html(e);
        $('#error-elem').fadeIn();
    }
}

$('#modalTarea').on('hidden.bs.modal', function () {
    location.reload()
});

// $("input:checked[name=tipo_tarea]:radio").change(function () {
//     console.log("ea")
//     // alert(this.value)
// })