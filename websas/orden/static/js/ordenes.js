var tabla_html = $('#datatable-ordenes');
var modal_observacion = $('#modal-observacion');
var modal_observacion_texto = $('#texto-observacion-completa');
var observaciones_truncadas = {};

// Truncate a string
function strtrunc(str, max, add){
    add = add || '... (ver todo)';
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
                    var obs_corta = strtrunc(data, 50);
                    var fila = meta.row;
                    observaciones_truncadas[fila] = data;
                    var prefijo = '<a href=# onclick="mostrar_observacion(\'' + fila + '\')">';
                    var sufijo = '</a>';
                    data = prefijo + obs_corta + sufijo;
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

function mostrar_observacion(clave) {
    modal_observacion_texto.html(observaciones_truncadas[clave]);
    modal_observacion.modal();
}