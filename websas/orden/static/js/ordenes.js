var tabla_html = $('#datatable-ordenes');

// Elipsis para observaciones muy largas...
function strtrunc(str, max, add){
    add = add || ' ...';
    return (typeof str === 'string' && str.length > max ? str.substring(0, max - add.length) + add : str);
 };

tabla_html.DataTable({
    responsive: true,
    dom: "Bfrtip",
    order: [[ 0, 'desc' ]],
    columnDefs: [
        {
            'targets': 2,
            'render': function(data, type, full, meta){
                if (data.length > 50){
                    return strtrunc(data, 50);
                }
                return data;                
            }
        }
    ],
    buttons: [{
        text: "<b>Nueva orden</b>",
        action: function() {
            // TODO: si es necesario generar el form de nuevo técnico
            // como modal, este botón puede dispararlo
            // Por ahora sólo pega a crear técnico
            location.href = "/orden/crear";
        },
        className: "btn-sm btn-info"
    }, {
        extend: "copy",
        text: "Copiar tabla",
        className: "btn-sm"
    }, {
        extend: "csv",
        text: "Exportar tabla a CSV",
        className: "btn-sm"
    }, {
        extend: "print",
        text: "Imprimir tabla",
        className: "btn-sm"
    }, ],
});


var chart

function init_grafico() {
    var fecha_ini = $("#daterangepicker").data('daterangepicker').startDate
    var fecha_fin = $("#daterangepicker").data('daterangepicker').endDate

    //copiamos las fechas porque si no se va a decrementando en un anio
    //cada vez que se envia el segundo dataset
    var fecha_ini_vieja = moment($("#daterangepicker").data('daterangepicker').startDate)
    var fecha_fin_vieja = moment($("#daterangepicker").data('daterangepicker').endDate)

    $("#fecha-ini").html(fecha_ini.format("DD/MM/YYYY"))
    $("#fecha-fin").html(fecha_fin.format("DD/MM/YYYY"))
    chart = $("#chart-container").reporteSAS({
        opcionesDataset: [
            {
                tipochart: 'column',
                x: '0',
                y: '1',
                dataset: "ordenes_total",
                textoLeyenda: "Facturado en el año actual",
                opcionesAjax: {
                    fecha_ini: fecha_ini.format("DD/MM/YYYY"),
                    fecha_fin: fecha_fin.format("DD/MM/YYYY"),
                    filtro: $("#id_filtros").val(),
                    ajaxurl: $("form")[0].dataset["ajax_url"],
                },
            },
            {
                tipochart: 'column',
                x: '0',
                y: '1',
                dataset: "ordenes_total",
                textoLeyenda: "Facturado en el año pasado",
                opcionesAjax: {
                    fecha_ini: fecha_ini_vieja.subtract(1, "year").format("DD/MM/YYYY"),
                    fecha_fin: fecha_fin_vieja.subtract(1, "year").format("DD/MM/YYYY"),
                    filtro: $("#id_filtros").val(),
                    ajaxurl: $("form")[0].dataset["ajax_url"],
                },
            },
        ],
        opcionesGrafico: {}
    });
}
$(document).on('ready', function () {
    return init_grafico()
})

$("form .chart-input").on("change", function () {
    chart.CanvasJSChart().destroy()
    return init_grafico()
})


$("#daterangepicker").on("apply.daterangepicker", function (ev, picker) {
    chart.CanvasJSChart().destroy()
    return init_grafico()
})
