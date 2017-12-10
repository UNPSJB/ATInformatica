(function ($) {
  'use strict'

  $.fn.extend({

    reporteSAS: function (opcionesUsuario) {

      var opcionesDataset = {
        tipochart : "",
        x : "x",
        y : "y",
        dataset : "dataset",
      }

      var opcionesAjax = {
        fecha_ini : '',
        fecha_fin : '',
        filtro : '',
        ajaxurl : '',
      }

      var opcionesGrafico = {
        titulo : '',
      }

      var opcionesIniciales = {
        'opcionesDataset': opcionesDataset,
        'opcionesAjax': opcionesAjax,
        'opcionesGrafico': opcionesGrafico
      }

      function inicializar(){
        var chartContainer = this

        var opc = $.extend(opcionesIniciales, opcionesUsuario)

        $.ajax({
          url: opc.opcionesAjax.ajaxurl,
          type: "GET",
          data: {
            "fecha_ini": opc.opcionesAjax.fecha_ini,
            "fecha_fin": opc.opcionesAjax.fecha_fin,
            "filtros": opc.opcionesAjax.filtro,
          },
          dataType: "json",
          success: function (data) {

            var dataPoints = [];
            
            for (let i = 0; i < data[opc.opcionesDataset.dataset].length; i++) 
            {

              dataPoints.push({
                x: data[opc.opcionesDataset.dataset][i][opc.opcionesDataset.x],
                y: data[opc.opcionesDataset.dataset][i][opc.opcionesDataset.y]
              })
              
            }  
              
            var chart = new CanvasJS.Chart(chartContainer, {
              title: {
                text: opc.opcionesGrafico.titulo
              },
              data: [{
                type: opc.opcionesDataset.tipochart,
                dataPoints: dataPoints,
              }]
            });
            return chart.render()
          },
          error: function(data){
            alert(data)
          }
        });
      }

      return $(this).each(inicializar)
    }
    
  })
})(jQuery)
