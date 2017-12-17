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
        "filtrar_en_cero": false,
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

        for(let i = 0; i < opc.opcionesDataset.length; i++) {
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
                    
                    for (let i = 0; i < data[ds.dataset].length; i++) {
                      var valor = parseFloat(data[ds.dataset][i][ds.y]);
                      dataPoints.push({
                        label: data[ds.dataset][i][ds.x],
                        name: data[ds.dataset][i][ds.x],
                        y: valor,
                      });
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

          // Filtrar si corresponde
          if (opc.opcionesGrafico.filtrar_en_cero) {
            // Aux
            var datapoints_en_cero = {};  // Contar para cada DP en cuántas series se encontró en 0
            var datapoints_borrar = [];   // Qué datapoints borrar de TODAS las series
            var cant_series = datasets.length;  // Número total de series

            // Determinar DPs en 0 - iterar en datasets para analizar datapoints
            datasets.forEach(function(este_dataset) {
              // Iterar en datapoints para registrar ocurrencias en cero
              este_dataset.dataPoints.forEach(function(este_dataPoint) {
                if (este_dataPoint.y == 0) {
                  // Agregar al contador de ocurrencias en cero
                  datapoints_en_cero[este_dataPoint.name] = datapoints_en_cero[este_dataPoint.name] ? datapoints_en_cero[este_dataPoint.name] + 1 : 1;
                  // Si conté que todos están en cero, marcarme para borrar
                  if (datapoints_en_cero[este_dataPoint.name] === cant_series) {
                    datapoints_borrar.push(este_dataPoint.name);
                  }
                }
              });
            });

            // Borrar DPs en 0
            // Iterar en datasets para borrarme de la lista de datapoints
            datasets.forEach(function(ds) {
              // Iterar en los datapoints marcados para borrar
              datapoints_borrar.forEach(function(dp) {
                // Buscar el elemento marcado
                var match = ds.dataPoints.find(x => x.name == dp);
                if (match != undefined) {
                  var i = ds.dataPoints.indexOf(match);
                  // Determinar el índice ^ y borrar:
                  ds.dataPoints.splice(i,1);
                }
              });
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
