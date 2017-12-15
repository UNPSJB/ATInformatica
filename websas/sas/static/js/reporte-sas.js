(function ($) {
  'use strict'
    
  var opcionesIniciales

  $.fn.extend({

    reporteSAS: function (opcionesUsuario) {

    //esto tendria que ser un arreglo, asi podemos tener varios dataset
    //en un mismo grafico
      var opcionesAjax = {
        "fecha_ini": '',
        "fecha_fin": '',
        "filtro": '',
        "ajaxurl": '',
      }

      var opcionesDataset = [{
          "tipochart" : "",
          "x" : "x",
          "y" : "y",
          "dataset" : "dataset",
          "textoLeyenda": "",
          "opcionesAjax": opcionesAjax,
        },
      ]

      var opcionesGrafico = {
        "titulo" : '',
        "mensaje_error" : "Su consulta no generó resultados",
        "nombre_eje_x": "",
        "nombre_eje_y": "",
      }

      opcionesIniciales = {
        'opcionesDataset': opcionesDataset,
        'opcionesGrafico': opcionesGrafico,
      }

        
      function inicializar(){
        
        var opc = $.extend(true, opcionesIniciales, opcionesUsuario)
        var datasets = []
        $(this).CanvasJSChart({
          title:{
            text: opc.opcionesGrafico.titulo,
          },
          axisX: {
            title: opc.opcionesGrafico.nombre_eje_x,
            interval: opc.opcionesGrafico.intervalo_eje_x,
          },
          axisY: {
            title: opc.opcionesGrafico.nombre_eje_y,
            interval: opc.opcionesGrafico.intervalo_eje_y,
          },
          legend: {
            horizontalAlign: "central",
            verticalAlign: "bottom",
            fontSize: 15,
          },
          data: [],
        })

        for(let i = 0; i < opc.opcionesDataset.length; i++){
            var ds = opc.opcionesDataset[i]
            $.ajax({
              url: ds.opcionesAjax.ajaxurl,
              type: "GET",
              data: {
                  //si preguntamos por el valor, el data tiene la propiedad, pero vacia
                  //si no preguntamos, el data ni siquiera tiene la propiedad
                "fecha_ini": ds.opcionesAjax.fecha_ini,
                "fecha_fin": ds.opcionesAjax.fecha_fin,
                "filtros": ds.opcionesAjax.filtro,
                "rubro": ds.opcionesAjax.rubro,
                "tipo_servicio": ds.opcionesAjax.tipo_servicio,
                "tipo_tarea": ds.opcionesAjax.tipo_tarea,
              },
              async:false,
              dataType: "json",
              success: function (data) {
                    console.log(data);
                    ds = opc.opcionesDataset[i]
                    
                    //de esta forma podemos verificar que el servidor
                    //nos devolvio datos de nuestra consulta exitosamente
                    if(data.hasOwnProperty(data[ds.dataset]) || 
                        data[ds.dataset].length == 0){
                        //no mostramos nada mejor
                        //alert(opc.opcionesGrafico.mensaje_error)
                        return
                    }

                    var dataPoints = [];
                    
                    for (let i = 0; i < data[ds.dataset].length; i++){
                      dataPoints.push({
                        label: data[ds.dataset][i][ds.x],
                        name: data[ds.dataset][i][ds.x],
                        y: parseInt(data[ds.dataset][i][ds.y]),
                      }) 
                    }
                    datasets.push({
                        type:ds.tipochart,
                        showInLegend:true,
                        legendText: ds.textoLeyenda,
                        dataPoints: dataPoints,
                    })
              },
              error: function(data){
                alert("error en ajax")
                console.log(data)
              },
            });
          }
          
          //cargamos los datos al grafico
          $(this).CanvasJSChart().options.data = datasets

          //renderizamos
          $(this).CanvasJSChart().render()
          return $(this).CanvasJSChart()
        }
      return $(this).each(inicializar)
      },
      refrescar: function(opcionesNuevas){

          /**
           * se complica actualizar el dataset porque ahora es un arreglo vistes
           */
          // $(this).CanvasJSChart().destroy()
          
          // //el true es para hacer un deepcopy
          // //https://api.jquery.com/jquery.extend/
          // var opc = $.extend(true, opcionesIniciales, opcionesNuevas)

          // return $(this).reporteSAS(opc)
      }
  })
})(jQuery)
