function agregarRol(){
    persona_id = $("#input-id-persona").val()
    rol = $("#input-tipo-rol").val()
    data = {
        
        'persona_id': persona_id,
        'rol': rol,
    }

    $.ajax({
        url: $("#btn-agregar-rol").attr("data-ajax-url"),
        type: "POST",
        data: data,
        dataType: 'json',
        success: function (res) {
            location.href = res.url
        },
        statusCode: {
            403: function(data) {
                mostrarError(data.responseJSON.error.__all__[0]);
            }
        }
    });
}

function mostrarError(mensaje) {
    $('#errormsg').html(mensaje);
    $('#error-elem').fadeIn();
}