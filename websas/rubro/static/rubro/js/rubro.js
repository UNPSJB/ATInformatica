var tabla = $("#datatable-rubros").DataTable({
    responsive: true,
    keys: true,
    dom: "Bfrtip",
    buttons: [{
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

// $('#datatable-rubros tbody').on('click', 'tr', function() {
//     var datosFila = tabla.row(this).data();
//     alert('Data: ' + datosFila);
// });