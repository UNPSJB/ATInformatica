var tabla = $("#datatable-tipo-tarea-tarifar").DataTable({
    responsive: true,
    keys: true,
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
    },],
});

var tarifas_actualizadas = []

$('#datatable-tipo-tarea-tarifar tbody').on('change', 'td', function () {

    //recuperamos el tipo de servicio
    var tipo_servicio = tabla.row(this).data()[0]
    //armamos el id de la celda y recuperamos el valor de la tarifa
    var id = "#tarifa_" + tipo_servicio.replace(/\s/g, '').toLowerCase()
    var precio = parseInt(tabla.cell(this).$(id).val())
    //recuperamos la pk de la tarifa
    if (isNaN(precio)){
        alert("No me ingresaste un precio maestro")
    }
    var tarifa = tabla.cell(this).$(id).attr("tarifa")

    //mandamos los datos al servidor
    $.ajax({
        //la url a donde hay que pegarle en el servidor esta en el html de la tabla
        //de esta forma, podemos tener el .js separado del .html
        url: $("#datatable-tipo-tarea-tarifar").attr("ajax-url"),
        type: "POST",
        data: {
            "tarifa": tarifa,
            "precio": precio
        },
        dataType: 'json',
        success: function (data) {
            console.log("enviado")
        }
    }) 

});

$("form").submit(function(e){});



/**
 * 
 * funciones para conseguir el token csrf
 * horrible que esto este aca, deberia moverselo mas arriba en la jerarquia
 * sacado de este sitio:
 * https://docs.djangoproject.com/en/dev/ref/csrf/
 */


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





function isNumberKey(event) {
    /**
     * Esta función no te deja ingresar en un submit caracteres que no sean
     * dígitos, el type "number" te los deja escribir, pero te valida antes de hacer el submit
     * 
     * Para agregarla a un submit, agregarle al html
     * 
     * onkeypress="return isNumberKey(event)"
     */

    var charCode = (event.which) ? event.which : event.keyCode
    if ((charCode > 31) && ((charCode) < 48) || (charCode > 57)) {
        return false
    }
    return true
}