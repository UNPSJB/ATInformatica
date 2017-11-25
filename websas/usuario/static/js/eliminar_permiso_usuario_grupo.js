$(" #eliminar-permiso-grupo, #eliminar-usuario-grupo ").on("click", function () {
    console.log(this)
    var data = {
        "grupo_id": this.dataset["grupo"],
        "valor": this.dataset["valor"],
    }
    $.ajax({
        url: this.dataset["ajax"],
        type: "POST",
        data: data,
        dataType: 'json',
        success: function (data) {
            location.reload()
        },
        error: function (data) {
        }
    })
})
