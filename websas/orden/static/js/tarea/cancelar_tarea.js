function confirmarCancelacionTarea(){
    $("#modal-cancelar-tarea").modal("toggle")
}


function cancelarTarea(){
    var tarea = $("#modal-cancelar-tarea")[0].dataset["id_tarea"]

    var data = {
        "tarea_id": tarea,
    }

    console.log()

    $.ajax({
        url: $("#cancelar_tarea")[0].dataset["ajax_url"],
        type: "POST",
        data: data,
        dataType: "json",
        success: function(data){
            $("#modal-cancelar-tarea").modal("toggle")
        }
    })
}

$('#modal-cancelar-tarea').on('hidden.bs.modal', function () {
    location.reload()
});
