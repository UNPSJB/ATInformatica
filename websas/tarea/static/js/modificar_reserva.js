function modificarReserva(){
    var reserva = $("#modal-detalle-reserva")[0].dataset["id_reserva"]
    var cantidad = parseInt($("#input-modificar-cantidad").val())

    if(isNaN(cantidad) || cantidad < 0){
        $("#cantidad-error").fadeIn()
        return
    }
    var data = {
        "reserva_id": reserva,
        "cantidad": cantidad,
    }
    $.ajax({
        url: $("#modal-detalle-reserva")[0].dataset['ajax_url'],
        type: "POST",
        data: data,
        dataType: "json",
        success: function(data){
            $("#cantidad-error").fadeOut()
            $("#modal-detalle-reserva").modal('toggle')
        },
    })
}

$('#modal-detalle-reserva').on('hidden.bs.modal', function () {
    location.reload()
});
