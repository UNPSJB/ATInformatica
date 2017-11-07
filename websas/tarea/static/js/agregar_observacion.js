function agregarObservacion(){   
    var data = {
        'tarea' : $('#modalObservacion').attr("data-tarea-id"),
        'contenido': $('textarea').val(),
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