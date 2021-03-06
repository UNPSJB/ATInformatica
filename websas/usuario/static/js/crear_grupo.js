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


function crearGrupo(){

    var nombre = $("input:text[name=nombre-grupo]").val() 
    if(!Boolean(nombre)){
        console.log("ahre")
        $("#errormsg").html("Debe ingresar un nombre")
        $("#error-elem").fadeIn()
        return
    }

    $("error-elem").fadeOut()
    data = {
        'name': nombre
    }
     
    $.ajax({    
        url: $('#btn-crear-grupo').attr('ajax-url'),
        type: "POST",
        data: data,
        dataType: 'json',
        success: function(data){
            $("#modalGrupo").modal("toggle")
            location.reload()    
        },
        statusCode: {
            403: function(data) {
                // Mensaje del servidor
                $("#errormsg").html("Error al crear el grupo " + "\"" + nombre + "\"")
                $("#error-elem").fadeIn()
            }
        }
    });

}