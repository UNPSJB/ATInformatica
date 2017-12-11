var chart
$(document).on('ready', function(){

    var fecha_ini = $("#daterangepicker").data('daterangepicker').startDate.format("DD/MM/YYYY")
    var fecha_fin = $("#daterangepicker").data('daterangepicker').endDate.format("DD/MM/YYYY")

    $("#fecha-ini").html(fecha_ini)
    $("#fecha-fin").html(fecha_fin)
    chart = $("#chart-container").reporteSAS({
        opcionesDataset: [
        {
            tipochart : 'column',
            x : 'criterio',
            y : 'total',
            dataset : "ordenes_total",
            textoLeyenda: "Facturado en el año actual",
        },
        {
            tipochart : 'column',
            x : 'criterio',
            y : 'total',
            dataset : "ordenes_viejas",
            textoLeyenda: "Facturado en el año pasado",
        },
        ],
        opcionesAjax : {
            fecha_ini : fecha_ini,
            fecha_fin : fecha_fin,
            filtro : $("#id_filtros").val(),
            ajaxurl : $("form")[0].dataset["ajax_url"],
        },
        opcionesGrafico: {
        }
      });
})

$("form .chart-input").on("change", function(){
    chart.refrescar({
        opcionesAjax : {
            filtro : $("#id_filtros").val(),
        },
    })
})


$("#daterangepicker").on("apply.daterangepicker", function(ev, picker){

    chart.refrescar({
        opcionesAjax : {
            fecha_ini : $("#daterangepicker").data('daterangepicker').startDate.format("DD/MM/YYYY"),
            fecha_fin : $("#daterangepicker").data('daterangepicker').endDate.format("DD/MM/YYYY"),
        },
    })
})
