function eliminarRol(){
    data = {
        'persona_id': $("#data-rol").attr("data-empleado-id"),
        'rol_id': $("#data-rol").attr("data-rol-id"),
    }

    $.ajax({
        url: $("#data-rol").attr("data-ajax-url"),
        type: "POST",
        data: data,
        dataType: 'json',
        success: function (res) {
            alert(res.url)
            if (res.url == '') {
                location.reload()
            }
            else {
                location.href = res.url
            }
        },
        error: function (data) {
            console.log(data)
            alert("Error")
            
        }
    });
}