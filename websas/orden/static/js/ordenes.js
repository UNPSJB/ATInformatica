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

// Registrar el onclick para la fila, excepto si no hay data, o si es
// la primera celda, que es la que expande las columnas ocultas por el
// comportamiento responsive del DataTable, el cual está bueno.
tabla_html.on(
    'click',
    'tbody tr td:not(".celda_control"):not(".dataTables_empty")',
    function(e) {
        var fila = $(this).parent();

        // Si la fila que clickeé es la expansión (child), no voy a encontrar la
        // URL en ella, sino en su inmediatamente anterior, lo cual está bueno.
        if (fila.hasClass("child")) {
            location.href = fila.prev().attr('data-tableclick');
        } else {    // Si no es child el dato está acá, lo cual está bueno también.
            location.href = fila.attr('data-tableclick');
        }
    }
);
