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

$('#form_equipo').submit(function(e){
    var could
    var data = {
        'nro_serie':$('#id_nro_serie').val(),
        'rubro':$('select#id_rubro').val(),
        'descripcion':$('#id_descripcion').val()
    }

    var rubro = data['rubro']
    
    console.log('lsdkfjsad')
    $.ajax({    

        //la url a donde hay que pegarle en el servidor esta en el html de la tabla
        //de esta forma, podemos tener el .js separado del .html
        url: '/orden/equipo/crear_json',
        method: "POST",
        data:data,
        success: function(data){
            window.opener.get_equipos(rubro)
            window.close()
            could = true
        }
    })
    return could
})



