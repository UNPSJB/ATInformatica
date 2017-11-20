
$(document).ready(function(){
    tabla_rubros()
})

// Inicializacion y referencia al DataTable, con la config ajax de cada columna
function tabla_rubros(){
    var tabla_html = $("#datatable-rubros")

    // Inicializacion y referencia al DataTable, con la config ajax de cada columna
    var dtabla = tabla_html.DataTable({
        "responsive": true,
        "autoWidth": false,
        "columns": [
            {"data": ""},
            {"data": "nombre"},
            {"data": "descripcion"},
        ],
        "dom": "Bfrtip",
        "buttons": [{
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

    console.log('dtabla')
    console.log(dtabla)
    return dtabla
}