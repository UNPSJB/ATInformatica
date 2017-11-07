$("#datatable-reservas").DataTable({
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

function reservarStock(){   
    var data = {
        'tarea' : $('#modalReserva').attr("data-tarea-id"),
        'producto': $('input:checked[name=producto]')[0].dataset['idproducto'],
        'cantidad': $('#cantidad').val(),
    }

    $.ajax({    
        url: $("#modalReserva").attr("ajax-url"),
        type: "POST",
        data: data,
        dataType: 'json',
        success: function(data){
            $('#modalReserva').modal('toggle');    
        }
    })
}

$('#modalReserva').on('hidden.bs.modal', function () {
    location.reload()
});
