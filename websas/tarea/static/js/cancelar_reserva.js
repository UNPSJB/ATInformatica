function confirmarCancelacionReserva(){
    $("#modal-cancelar-reserva").modal("toggle")
}


function cancelarReserva(){
    var reserva = $("#modal-cancelar-reserva")[0].dataset["id_reserva"]

    var data = {
        "reserva_id": reserva,
    }

    $.ajax({
        url: $("#cancelar_reserva")[0].dataset["ajax_url"],
        type: "POST",
        data: data,
        dataType: "json",
        success: function(data){
            $("#modal-cancelar-reserva").modal("toggle")
        },
        statusCode: {
            403: function(data) {
                // Mensaje del servidor
                mostrarError(data.responseJSON.error);
            }
        }
    })
}

function mostrarError(mensaje) {
    $('#errormsg').html(mensaje);
    $('#error-elem').fadeIn();
}

$('#modal-cancelar-reserva').on('hidden.bs.modal', function () {
    location.reload()
});
