$("#btn-ajax").on("click", function(){

    var picker = $("#daterangepicker").data('daterangepicker')
    var fecha_ini = picker.startDate.format("DD/MM/YYYY")
    var fecha_fin = picker.endDate.format("DD/MM/YYYY")
    var filtro = $("#id_filtros").val()

    $.ajax({
        url: $("form")[0].dataset["ajax_url"],
        type: "GET",
        data: {
            "fecha_ini": fecha_ini,
            "fecha_fin": fecha_fin,
            "filtros": filtro,
        },
        dataType: "json",
        success: function(data){
            console.log(data)
        }
    })
})
