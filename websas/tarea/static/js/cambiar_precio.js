function cambiarPrecio() {

    var precio = parseInt($("#precio").val())

    if(isNaN(precio) || precio < 0){
        $("#precio-error").html("Debe ingresar un válido")
        return
    }

    var data = {
        'tarea' : $('#modalCambiarPrecio').attr("data-tarea-id"),
        'precio': precio
    }


    $.ajax({
        url: $("#modalCambiarPrecio").attr("ajax-url"),
        type: "POST",
        data: data,
        dataType: 'json',
        success: function (data) {
            $('#modalCambiarPrecio').modal('toggle');            
        }
    })

}

$('#modalCambiarPrecio').on('hidden.bs.modal', function () {
    location.reload()
});

function texto_observacion(){
  var texto = $('#editor-one').html().replace(/<br>/g,'')
  .replace(/<div>/g,'\n').replace(/<\/div>/g, '')
  .replace(/&lt;/g, '<').replace(/&gt;/g, '>')
  .replace(/<code>/g,'').replace(/<\/code>/g,'')

  return texto
}
