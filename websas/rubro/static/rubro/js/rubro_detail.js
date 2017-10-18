var tabla = $("#datatable-rubro-detail").DataTable({
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
    }, ],
});

$('#datatable-rubro-detail tbody').on('change', 'td', function() {

    //recuperamos la tarea y el tipo de servicio de la celda
    var tarea = tabla.row(this).data()[0];
    var tipoServicio = $(tabla.column(this).header()).html();
    
    //armamos el id de la celda, con el indice de la fila y de la columna
    var iFila = tabla.row(this).index();
    var iCol = tabla.column(this).index()
    var id = "#" + iFila + iCol
    
    //recuperamos el precio de la celda
    var precio = tabla.cell(this).$(id).val()

    // console.log($("datatable-rubro-detail").attr("ajax-url"))
    
    //mandamos los datos al servidor
    $.ajax({    
        //la url a donde hay que pegarle en el servidor esta en el html de la tabla
        //de esta forma, podemos tener el .js separado del .html
        url: $("#datatable-rubro-detail").attr("ajax-url"),
        type: "POST",
        data: {
            "tarea": tarea,
            "tipo_servicio": tipoServicio,
            "precio": precio
        },
        dataType: 'json',
        success: function(data){
            console.log("en la success function");
            console.log(data)
        }
    })
});




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
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});





// $('#datatable-rubro-detail tbody').on('click', 'td', function() {
//     var tarea = tabla.row(this).data()[0];

//     //estos dos indices se usan por lo pronto para ver la fila y columna,
//     //pero si no, estan de mas
//     var iFila = tabla.row(this).index();
//     var iCol = tabla.column(this).index()
    
//     var tipoServicio = $(tabla.column(this).header()).html();

//     // var precio = $(tabla.cell(this).data()).val()
//     var precio = tabla.cell(this).$(":input:focus").val()
    
    
    
//     console.log("celda " + iFila +", " + iCol)
//     console.log('Tarea: ' + tarea + ", " + "Tipo de servicio: " + tipoServicio);
//     // console.log("Precio: " + precio)
//     console.log(precio)
// });


function isNumberKey(event){
    /**
     * Esta función no te deja ingresar en un submit caracteres que no sean
     * dígitos, el type "number" te los deja escribir, pero te valida antes de hacer el submit
     * 
     * Para agregarla a un submit, agregarle al html
     * 
     * onkeypress="return isNumberKey(event)"
     */

    var charCode = (event.which) ? event.which : event.keyCode
    if ((charCode > 31) && ((charCode) < 48) || (charCode > 57)){
        return false
    }
    return true
}