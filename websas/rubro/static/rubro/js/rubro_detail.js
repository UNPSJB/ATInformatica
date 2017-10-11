var tabla = $("#datatable-rubro-detail").DataTable({
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

$('#datatable-rubro-detail tbody').on('change', 'td', function() {
    var tarea = tabla.row(this).data()[0];

    //estos dos indices se usan por lo pronto para ver la fila y columna,
    //pero si no, estan de mas
    var iFila = tabla.row(this).index();
    var iCol = tabla.column(this).index()
    // var iCelda = (iFila*10) + iCol
    var tipoServicio = $(tabla.column(this).header()).html();


    /**
     * tenemos que conseguir el input del elemento que recien cambio
     * el loco me junta todos los inputs de las celdas, y nada que ver
     */
    
    // console.log(iCelda)
    // var precio = $(tabla.cell(this).data()).val()
    // var precio = tabla.cell(this).$(":input:not(:focus)").val()
    // var precio = tabla.cell(this).$(":input:eq("+iCelda+")").val()
    
    
    
    console.log("celda " + iFila +", " + iCol)
    console.log('Tarea: ' + tarea + ", " + "Tipo de servicio: " + tipoServicio);
    // console.log("Precio: " + precio)
    console.log(precio)
});




// $('#datatable-rubro-detail tbody').on('click', 'td', function() {
//     var tarea = tabla.row(this).data()[0];

//     //estos dos indices se usan por lo pronto para ver la fila y columna,
//     //pero si no, estan de mas
//     var iFila = tabla.row(this).index();
//     var iCol = tabla.column(this).index()
    
//     var tipoServicio = $(tabla.column(this).header()).html();

//     // var precio = $(tabla.cell(this).data()).val()
//     var precio = tabla.cell(this).$(":input:focus").val()
    
    
    
//     console.log("celda " + iFila +", " + iCol)
//     console.log('Tarea: ' + tarea + ", " + "Tipo de servicio: " + tipoServicio);
//     // console.log("Precio: " + precio)
//     console.log(precio)
// });


function isNumberKey(event){
    /**
     * Esta función no te deja ingresar en un submit caracteres que no sean
     * dígitos, el type "number" te los deja escribir, pero te valida antes de hacer el submit
     * 
     * Para agregarla a un submit, agregarle al html
     * 
     * onkeypress="return isNumberKey(event)"
     */

    var charCode = (event.which) ? event.which : event.keyCode
    if ((charCode > 31) && ((charCode) < 48) || (charCode > 57)){
        return false
    }
    return true
}