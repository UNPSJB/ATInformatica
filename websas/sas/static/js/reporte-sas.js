(function ($) {
  'use strict'
    
    var opcionesIniciales

  $.fn.extend({

    reporteSAS: function (opcionesUsuario) {

    //esto tendria que ser un arreglo, asi podemos tener varios dataset
    //en un mismo grafico
        var opcionesDataset = [{
            tipochart : "",
            x : "x",
            y : "y",
            dataset : "dataset",
            textoLeyenda: "",
        },]

      var opcionesAjax = {
        fecha_ini : '',
        fecha_fin : '',
        filtro : '',
        ajaxurl : '',
      }

      var opcionesGrafico = {
        titulo : '',
        mensaje_error : "Su consulta no generó resultados",
      }

      opcionesIniciales = {
        'opcionesDataset': opcionesDataset,
        'opcionesAjax': opcionesAjax,
        'opcionesGrafico': opcionesGrafico,
      }

        
      function inicializar(){
        var chartContainer = this

        var opc = $.extend(true, opcionesIniciales, opcionesUsuario)

        $.ajax({
          url: opc.opcionesAjax.ajaxurl,
          type: "GET",
          data: {
              //si preguntamos por el valor, el data tiene la propiedad, pero vacia
              //si no preguntamos, el data ni siquiera tiene la propiedad
            "fecha_ini": opc.opcionesAjax.fecha_ini,
            "fecha_fin": opc.opcionesAjax.fecha_fin,
            "filtros": opc.opcionesAjax.filtro,
          },
          dataType: "json",
          success: function (data) {

              var datasets = []
              console.log(data)
              for(let i = 0; i < opc.opcionesDataset.length; i++){

                  var ds = opc.opcionesDataset[i]

                  //console.log("ds: ")
                  //console.log(ds)

                  //de esta forma podemos verificar que el servidor
                  //nos devolvio datos de nuestra consulta exitosamente
                  if(data.hasOwnProperty(data[ds.dataset]) || 
                      data[ds.dataset].length == 0){
                      alert(opc.opcionesGrafico.mensaje_error)
                      return
                  }

                var dataPoints = [];
                
                for (let i = 0; i < data[ds.dataset].length; i++) 
                {

                  dataPoints.push({
                    label: data[ds.dataset][i][ds.x],
                    y: parseInt(data[ds.dataset][i][ds.y])
                  })
                  
                }  
                  
                datasets.push({
                    type:ds.tipochart,
                    showInLegend:true,
                    legendText: ds.textoLeyenda,
                    dataPoints: dataPoints,
                })

              }

            var chart = $(chartContainer).CanvasJSChart({
              title: {
                text: opc.opcionesGrafico.titulo
              },
              data: datasets, 
            });
            return chart

          },
          error: function(data){
            alert("error en ajax")
            console.log(data)
          }
        });



      }
      return $(this).each(inicializar)
    },
    refrescar: function(opcionesNuevas){
        $(this).CanvasJSChart().destroy()
        
        //el true es para hacer un deepcopy
        //https://api.jquery.com/jquery.extend/

        var opc = $.extend(true, opcionesIniciales, opcionesNuevas)
        return $(this).reporteSAS(opc)
    }
  })
})(jQuery)
