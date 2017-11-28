$(document).ready(function(){
    tabla_tecnicos()
})

// Inicializacion y referencia al DataTable, con la config ajax de cada columna
function tabla_tecnicos(){
    var tabla_html = $("#datatable-tecnicos")

    // Inicializacion y referencia al DataTable, con la config ajax de cada columna
    var dtabla = tabla_html.DataTable({
        // "ajax": {'url':'localhost:8000/orden/lista_clientes'},//tabla_html.attr('data-ajax_url'),
        "autoWidth": false,
        "columns": [
            {"data":""},
            {"data": "nombre"},
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

    // Click en la fila para seleccionar
    tabla_html.on('click', 'tr', function() {
        var radio = $(this).find('input');
        if (radio[0]) {
            dtabla.$('tr.row_selected').removeClass('row_selected');
            $(this).addClass('row_selected');
            radio.iCheck('checked');
        }
    });
    
    return dtabla
}