$("#datatable-producto").DataTable({
    responsive: true,
    dom: "Bfrtip",
    buttons: [{
        text: "<b>Nuevo producto</b>",
        action: function() {
            // TODO: si es necesario generar el form de nuevo técnico
            // como modal, este botón puede dispararlo
            // Por ahora sólo pega a crear técnico
            location.href = "/producto/crear";
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