function confirmarCancelacionReserva(){
    $("#modal-cancelar-reserva").modal("toggle")
}


function cancelarReserva(){
    var reserva = $("#modal-cancelar-reserva")[0].dataset["id_reserva"]

    var data = {
        "reserva_id": reserva,
    }

    console.log()

    $.ajax({
        url: $("#cancelar_reserva")[0].dataset["ajax_url"],
        type: "POST",
        data: data,
        dataType: "json",
        success: function(data){
            $("#modal-cancelar-reserva").modal("toggle")
        }
    })
}

$('#modal-cancelar-reserva').on('hidden.bs.modal', function () {
    location.reload()
});
