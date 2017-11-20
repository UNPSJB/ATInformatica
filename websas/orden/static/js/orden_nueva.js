

// Inicializacion Smart Wizard
$('#creacion_ot').smartWizard({
    labelNext:'Siguiente',
    labelPrevious:'Anterior',
    labelFinish:'Finalizar',
    onLeaveStep: function(obj, context){
        console.log("Leaving step " + context.fromStep + " to go to step " + context.toStep);
        $('.ot_aviso').addClass('hidden')

        return true;
    },
    onFinish: crearOrden,
    fixHeight: false

});

$(function() {
    $('#creacion_ot').fadeIn();
    $('#creacion_ot').smartWizard('fixHeight');
});

function texto_observacion(){
  var texto = $('#editor-one').html().replace(/<br>/g,'')
  .replace(/<div>/g,'\n').replace(/<\/div>/g, '')
  .replace(/&lt;/g, '<').replace(/&gt;/g, '>')
  .replace(/<code>/g,'').replace(/<\/code>/g,'')

  return texto
}

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
    // Validaciones para crear OT
    var inputcliente = $('input:checked[name=cliente]')[0]
    var inputtecnico = $('input:checked[name=tecnico]')[0]
    var inputservicio = $('input:checked[name=tipo_servicio]')[0]
    var inputrubro = $('input:checked[name=rubro]')[0]
    var inputequipo = $('input:checked[name=equipo]')[0]
    var observacion = $('#editor-one').html()

    // Si marcó que va sin equipo
    if ($('#sinequipo').is(':checked')) {
        // Objeto auxiliar para pasar data "sin equipo"
        inputequipo = {'dataset': {'idequipo': 'sin'}}
    }

    var inputs = [inputcliente,inputtecnico,inputservicio, inputservicio,inputrubro,inputequipo]

    for (var i in inputs){
        if (!inputs[i]) {
            $('.ot_aviso').removeClass('hidden')
            return 0
        }
    }
    
    var data = {
        'cliente':inputcliente.dataset['idcliente'],
        'tecnico':inputtecnico.dataset['idtecnico'],
        'servicio':inputservicio.dataset['idtiposervicio'],
        'rubro':inputrubro.dataset['idrubro'],
        'equipo':inputequipo.dataset['idequipo'],
        'observacion':observacion
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
            location.href = '/orden/listar'
        }
    })
}
