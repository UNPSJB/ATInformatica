// Registrar el onclick para la fila en las tablas .tableclick,
// excepto si no hay data, o en la .celda_control, que es la que expande las
// columnas ocultas por el responsiveness del DataTable, lo cual está bueno.
$(document).ready(function() {
    $('.tableclick').each(function(e) {
        $(this).on(
            'click',
            'tbody tr td:not(".celda_control"):not(".dataTables_empty"):not(".celda_input")',
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
    });
});