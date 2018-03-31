$(document).ready(function()
{
  var json = $.getJSON("/app/api/fusionBarras");
  json.done(function(data){fusionBarras(data);});
  //FIN
  //Funcion Cargar Datos fusionBarras
   function fusionBarras(responseData){
      FusionCharts.ready(function () 
      {
          var revenueChart = new FusionCharts(
          {
            type: 'column2d',
            renderAt: 'chart-container',
            width: '500',
            height: '350',
            dataFormat: 'json',
            dataSource: responseData,
            "events": 
            {
                    "dataPlotClick": function (eventObj, dataObj) 
                    {
                      fusionCircular(dataObj);
                    }
            }
          }).render();
      });
   }
  //FIN
  //Funcion Cargar Datos fusionCircular
   function fusionCircular(responseData)
   { 
    FusionCharts.ready(function () 
    {
        $.getJSON("/app/api/fusionCircular", function(result)
        {
          //console.log(result)
          for(var i in result.ingresos){

            if(responseData['categoryLabel'] == result.ingresos[i].name)
            {
            var revenueChart = new FusionCharts(
            {
              type: 'doughnut2d',
              renderAt: 'chart-container1',
              width: '450',
              height: '450',
              dataFormat: 'json',
              dataSource: {"chart": result.chart, "data": result.ingresos[i].data}
             }).render();
             revenueChart.setChartAttribute('defaultcenterlabel',"Ingresos Totales: $ " + responseData['value']);
             break;
            }
          }
        });
      });
   }
   //FIN
});