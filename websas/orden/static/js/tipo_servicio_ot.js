
$(document).ready(function(){
    tabla_tipo_servicio()
})



// Inicializacion y referencia al DataTable, con la config ajax de cada columna
function tabla_tipo_servicio(){

    var tabla_html = $("#datatable-servicios")

    // Inicializacion y referencia al DataTable, con la config ajax de cada columna
    var dtabla = tabla_html.DataTable({
        "responsive": true,
        // "ajax": {'url':'localhost:8000/orden/lista_clientes'},//tabla_html.attr('data-ajax_url'),
        "columns": [
            {"data":""},
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