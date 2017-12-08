function imprimir(){
    // Init doc
    var doc = new jsPDF({
        orientation: 'p',
        unit: 'mm'
    });
    
    // Funciones auxiliares para centrar texto en la página
    var centrar_punto = function(text, x, y) {
        var textWidth = doc.getStringUnitWidth(text) * doc.internal.getFontSize() / doc.internal.scaleFactor;
        var textOffset = x - (textWidth / 2);
        doc.text(textOffset, y, text);
    }
    var centrar_ancho = function(text, y) {
        var textWidth = doc.getStringUnitWidth(text) * doc.internal.getFontSize() / doc.internal.scaleFactor;
        var textOffset = doc.internal.pageSize.width - (textWidth / 2);
        doc.text(textOffset, y, text);
    }


    /**
     * Cabecera BEGIN
     */
    doc.setFontSize(17);
    doc.setFillColor(24,40,24);
    doc.rect(15,0,doc.internal.pageSize.width, 10, 'F');

    // // Cargar logo
    // function getBase64Image(img) {
        
    //     var canvas = document.createElement("canvas");
    
    //     canvas.width = img.width;
    //     canvas.height = img.height;

    //     var ctx = canvas.getContext("2d");
    
    //     ctx.drawImage(img, 0, 0);
    
    //     var dataURL = canvas.toDataURL("image/png", 0.6);
    //     return dataURL;
    // }

    // var imagen = new Image();

    // imagen.onload = function() {
    //     var dataURI = getBase64Image(imagen);
    //     // Agregar la imagen resultante
    //     doc.addImage(dataURI, 'PNG', 0, 0, 25, 25);
    //     return dataURI;
    // }

    // imagen.src = '/static/images/AT-logo.jpg';

    /**
     * Cabecera END
     */


     /**
      * TÍTULO GENERAL PÁGINA
      */
    var titulo_general = 'Total facturado por cliente\nen el período ' + $('#fecha-ini').text() + ' al ' + $('#fecha-fin').text() + ':';
    doc.setFontSize(20);
    doc.text(30, 30, titulo_general);


    /**
     * GRAFICO 1 (LEFT)
     */
    // Get Grafico
    var canvasChart1 = $("#chart-total-ots")[0];
    var canvasImg1 = canvasChart1.toDataURL("image/png", 0.6);

    // Get Titulo
    var titulo_graf1 = 'Titulo Graf 1'

    // PRINT Titulo
    centrar_punto(titulo_graf1, 55, 65)

    // PRINT Grafico
    doc.addImage(canvasImg1, 'PNG', 20, 80, 90, 90);


    /**
     * GRAFICO 2 (RIGHT)
     */
    // Get Grafico
    var canvasChart2 = $("#chart-total-ots")[0];
    var canvasImg2 = canvasChart2.toDataURL("image/png", 0.6);

    // Get Titulo
    var titulo_graf2 = 'Titulo Graf 2'

    // PRINT Titulo
    centrar_punto(titulo_graf2, 150, 65)

    // PRINT Grafico
    doc.addImage(canvasImg2, 'PNG', 115, 80, 90, 90);    


    /**
     * TABLA (INF)
     */
    // Get Tabla
    var canvasChart = $("#chart-total-ots")[0];
    var canvasImg = canvasChart.toDataURL("image/png", 0.6);

    // Get Titulo
    var titulo_graf2 = 'Titulo Graf 2'

    // PRINT Titulo
    centrar_punto(titulo_graf2, 150, 65)

    // PRINT Grafico
    doc.addImage(canvasImg, 'PNG', 115, 80, 90, 90);    


    doc.save('prueba.pdf');
}