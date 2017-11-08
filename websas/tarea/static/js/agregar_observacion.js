function agregarObservacion(){   
    var data = {
        'tarea' : $('#modalObservacion').attr("data-tarea-id"),
        'contenido': texto_observacion(),
    }

    console.log(data);

    $.ajax({    
        url: $("#modalObservacion").attr("ajax-url"),
        type: "POST",
        data: data,
        dataType: 'json',
        success: function(data){
            $('#modalObservacion').modal('toggle');    
        }
    })
}

$('#modalObservacion').on('hidden.bs.modal', function () {
    location.reload()
});

function texto_observacion(){
  var texto = $('#editor-one').html().replace(/<br>/g,'')
  .replace(/<div>/g,'\n').replace(/<\/div>/g, '')
  .replace(/&lt;/g, '<').replace(/&gt;/g, '>')
  .replace(/<code>/g,'').replace(/<\/code>/g,'')

  return texto
}
