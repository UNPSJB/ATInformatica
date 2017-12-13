
/**
 * Interfaz:
 * imprimirPDF({
 *  membrete: [string] // \n hace newline
 *  titulo: [string],
 *  tiles: [tile[]]
 *  usuario: [string]
 * })
 * 
 * tile = {
 *  tipo: [string] = 'vacio' | 'grafico' | 'div_html' | 'cod_html'
 *  titulo: [string]
 *  selector: [string]
 *  html: [string]
 *  ancho: [boolean]
 * }
 */
function imprimirPDF(contenido_rep){
    var contenido_default = {
        membrete: 'AT Informática\nFragata Hércules 596\nPuerto Madryn (9120) - Chubut\nTel: (0280) 4456800',
        titulo: '', // Título del reporte
        tiles: [    // Lista de tiles
            {
                tipo: 'vacio'
            },
        ],
        usuario: '[usuario]',   // Usuario que solicitó el reporte
        fechahora: '01/01/2007 00:00'   // Fecha y hora (placeholder, se pone automáticamente en now())
    };

    // Mergear opciones
    var contenido = $.extend(contenido_default, contenido_rep);

    // Init doc
    var doc = new jsPDF({
        orientation: 'p',
        unit: 'mm'
    });
    
    // Funciones auxiliares para alinear texto
    var centrar_punto = function(text, x, y) {
        var textWidth = doc.getStringUnitWidth(text) * doc.internal.getFontSize() / doc.internal.scaleFactor;
        var textOffset = x - (textWidth / 2);   // Centrar 
        doc.text(textOffset, y, text);
    }
    var centrar_ancho = function(text, y) {
        var textWidth = doc.getStringUnitWidth(text) * doc.internal.getFontSize() / doc.internal.scaleFactor;
        // Me caga esta cuenta matemática:
        var textOffset = (doc.internal.pageSize.width / 2) - (textWidth / 3);   // Centrar según el ancho de la página
        doc.text(textOffset, y, text);
    }
    var derecha_punto = function(text, x, y) {
        var textWidth = doc.getStringUnitWidth(text) * doc.internal.getFontSize() / doc.internal.scaleFactor;
        var textOffset = x - textWidth;   // Alinear a la derecha
        doc.text(textOffset, y, text);
    }

    /**
     * Cabecera BEGIN
     * Rectángulo oscuro
     */
    // Agregar logo (hardcode por ahora)
    doc.addImage('data:image/jpeg;base64,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', 'JPG', 0, 2, 25, 20);
    
    // Texto para el "membrete"
    doc.setFontSize(10);
    doc.text(contenido['membrete'], 35, 8);

    // Línea horizontal del encabezado
    doc.line(10, 27, 200, 27);
        


     /**
      * TÍTULO GENERAL PÁGINA
      * TODO: multilínea
      */
    var titulo_general = contenido['titulo'];
    doc.setFontSize(22);
    centrar_ancho(titulo_general, 30);  // Centrar en la página


    doc.setFontSize(16);
    
        
    // Posición inicial del cursor
    var margen_izquierdo = 30;
    var cursor_graficos = {x: margen_izquierdo, y: 60};
        
    // Procesar los tiles
    contenido.tiles.forEach(function(tile) {
        // Es ancho? Setear tamaño_x para los dos tipos
        var tamaño_x = 85;
        var desplazamiento_cursor = {x: 90, y: 0};

        if (tile.ancho) {
                tamaño_x = tamaño_x * 1.8;
                desplazamiento_cursor.x = 0;
                desplazamiento_cursor.y = 90;
        }
        var tamaño_y = 80;  // Fijo.

        // Imprimir el título en la posición del cursor y desplazarlo hacia abajo
        if (tile.titulo) {
            doc.setFontSize(16);
            centrar_punto(tile.titulo, cursor_graficos.x + tamaño_x / 2, cursor_graficos.y);
            cursor_graficos.y = cursor_graficos.y + 8;
        }

        // Si soy un gráfico, pasarme a base64 y agregarme bajo el cursor
        if (tile.tipo == 'grafico') {
            var canvas = ($(tile.selector).find('canvas').first()[0]);
            var canvasImg = canvas.toDataURL();

            // Sección de cuentas matemáticas para escalar proporcionalmente los gráficos
            var alto = canvas.height;
            var ancho = canvas.width;

            // Relación de aspecto del gráfico (proporción ancho/alto)
            var rel_grafico_ancho = ancho / alto;
            var rel_grafico_alto = alto / ancho;

            // Variables para calcular la nueva posición del gráfico
            var offset_pos_x = 0, offset_pos_y = 0, nuevo_tamaño_x = tamaño_x, nuevo_tamaño_y = tamaño_y;

            // Relación de aspecto del tile
            var rel_tile = tile.ancho ? 2 : 1;

            // Si el gráfico es menos ancho que mi tile, fijar la altura y ver en cuánto cambio su ancho
            // para la inserción según el tamaño del tile
            if (rel_grafico_ancho <= rel_tile) {
                // Determinar ancho nuevo basado en la altura fijada (tamaño_y)
                nuevo_tamaño_x = tamaño_y * rel_grafico_ancho;
                // Calcular nueva posición para centrar imagen
                offset_pos_x = (tamaño_x - nuevo_tamaño_x) / 2;
            } else {    // Si el gráfico es más ancho que mi tile, fijo el ancho al máximo y modifico la altura
                // Determinar alto nuevo basado en el ancho fijado (tamaño_x)
                nuevo_tamaño_y = tamaño_x * rel_grafico_alto;
                
                // Calcular nueva posición para centrar imagen
                offset_pos_y = (tamaño_y - nuevo_tamaño_y) / 2;
            }

            // Poner la maldita cosa en el reporte:
            doc.addImage(canvasImg, 'PNG', cursor_graficos.x + offset_pos_x, cursor_graficos.y + offset_pos_y, nuevo_tamaño_x, nuevo_tamaño_y);

        } else if (tile.tipo == 'div_html' || tile.tipo == 'cod_html') {   // Si tengo HTML, escupirlo en la hoja
            var fuenteHTML;
            if (tile.tipo == 'div_html') {
                fuenteHTML = $(tile.selector).html();
            } else {
                fuenteHTML = tile['html'];
            }
            doc.fromHTML(
                fuenteHTML,
                cursor_graficos.x,
                cursor_graficos.y,
                {
                'width': tamaño_x, 
                'height': tamaño_y,
                'elementHandlers': {
                    '.no_imprimir': function(element, renderer) {
                        return true;
                        }
                    }
                }
            );          
        }

        cursor_graficos.x = cursor_graficos.x + desplazamiento_cursor.x;
        if (cursor_graficos.x > 120) {
            cursor_graficos.x = margen_izquierdo;
            desplazamiento_cursor.y = 90;
        }

        cursor_graficos.y = cursor_graficos.y + desplazamiento_cursor.y;
    });
    

    // Línea horizontal del pie de página
    doc.line(10, 285, 200, 285);

    // Pie de página
    var currentdate = new Date(); 
    var datetime = currentdate.getDate() + "/"
                + (currentdate.getMonth()+1)  + "/" 
                + currentdate.getFullYear() + " @ "  
                + currentdate.getHours() + ":"  
                + currentdate.getMinutes() + ":" 
                + currentdate.getSeconds();

    doc.setFontSize(10);
    doc.text(contenido['usuario'], 50, 290);
    derecha_punto(datetime, 205, 290);

    doc.save('prueba.pdf');
}