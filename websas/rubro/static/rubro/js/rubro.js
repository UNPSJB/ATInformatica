var tabla = $("#datatable-rubros").DataTable({
    responsive: true,
    keys: true,
    dom: "Bfrtip",
    buttons: [{
        text: "<b>Nuevo servicio</b>",
        action: function() {
            // TODO: si es necesario generar el form de nuevo técnico
            // como modal, este botón puede dispararlo
            // Por ahora sólo pega a crear técnico
            location.href = "/servicio/crear";
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

console.log("AHREEEEEEEe")
$('#datatable-rubros tbody').on('click', 'tr', function() {
    var datosFila = tabla.row(this).data();
    console.log("AHRE")
    alert('Data: ' + datosFila);
});