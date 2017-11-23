$("#datatable-equipo").DataTable({
    responsive: true,
    dom: "Bfrtip",
    buttons: [{
        text: "<b>Nuevo equipo</b>",
        action: function() {
            location.href = "crear";
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