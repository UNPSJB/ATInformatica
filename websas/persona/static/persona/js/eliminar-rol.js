function eliminarRol(rol_id){
    data = {
        'persona_id': $("#data-rol").attr("data-empleado-id"),
        'rol_id': rol_id, 
    }

    console.log(data)

    $.ajax({
        url: $("#data-rol").attr("data-ajax-url"),
        type: "POST",
        data: data,
        dataType: 'json',
        success: function (res) {
            if (res.url == '') {
                location.reload()
            }
            else {
                location.href = res.url
            }
        },
        error: function (data) {
            console.log(data)
            
            
        }
    });
}