var jsonCircular3DAgencias;
var jsonBarrasProductos;
var jsonLinesGeneral;
var jsontodoProductos;
var jsontodoAgencias;

$(document).ready(function()
{
     myFunction();
});

function myCargarJson(anio)
{
    jsonCircular3DAgencias = $.getJSON("/app/api/fusionCircular3DAgencias/"+anio);
    jsonBarrasProductos = $.getJSON("/app/api/fusionBarrasProductos/"+anio);
    jsonLinesGeneral = $.getJSON("/app/api/fusionLinesGeneral/"+anio);
    jsontodoProductos = $.getJSON("/app/api/todoProductos/");
    jsontodoAgencias = $.getJSON("/app/api/mapAgencias/");

    jsonCircular3DAgencias.done(function(data){
    fusionCircular3DAgencias(data);
});
    jsontodoProductos.done(function(data){
        fusiontodoProductos(data);
});
    jsonLinesGeneral.done(function(data){
    fusionLinesGeneral(data);
});
}


function myFunction() {
    var anio = $("#selectAnio").val();
    if ((anio != 0)){
      document.getElementById('container-agencias').innerHTML='';
      document.getElementById('container-barras-productos').innerHTML='';
      document.getElementById('container-lines-general').innerHTML='';
      myCargarJson(anio);
    }
    else{
      document.getElementById('container-agencias').innerHTML='';
      document.getElementById('container-barras-productos').innerHTML='';
      document.getElementById('container-lines-general').innerHTML='';
    }
}

function fusiontodoProductos(responseData){
    var id_productos = [];
    var acum = 0;        
    for(i in responseData['productos']){
        var id = 0;
        id = parseInt(responseData['productos'][acum]['id']);
        id_productos.push(id);
        acum = acum + 1;
      }
  jsontodoAgencias.done(function(data){
        fusiontodoAgencias(data,id_productos);
});   
}

function fusiontodoAgencias(responseData,id_productos){
    var id_agencias = [];
    var acum = 0;     
    for(i in responseData['agencias']){
        var id = 0;
        id = parseInt(responseData['agencias'][acum]['id']);
        id_agencias.push(id);
        acum = acum + 1;
      }
   jsonBarrasProductos.done(function(data){
      fusionBarrasProductos(data,id_productos,id_agencias);
  }); 
}

function fusionCircular3DAgencias(responseData)
   {
    var series_datos = [];
    for (var i =0 ; i<=responseData['data'].length-1 ;i++)
    {
        var datos = [];
        datos.push(responseData['data'][i]['label'],parseInt(responseData['data'][i]['value']));
        series_datos.push(datos);
    }
    Highcharts.chart('container-agencias', {
    chart: {
        type: 'pie',
        options3d: {
            enabled: true,
            alpha: 45,
            beta: 0
        }
    },
    title: {
        text: 'Agencias en General'
    },
    tooltip: {
        pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
    },
    plotOptions: {
        pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            depth: 35,
            dataLabels: {
                enabled: true,
                format: '{point.name}'
            }
        }
    },
    series: [{
        type: 'pie',
        name: 'Porcentaje de Ingresos ',
        data: series_datos
    }]
});
   }  

function fusionBarrasProductos(responseData,id_productos,id_agencias)
   {
    var datos_arreglo = [0,0,0,0,0,0,0,0,0,0,0,0];
    var series_datos = [];
    var datos = {};
    var nombre_agencia = "";
    var stack_ID_agencia = 0;
    for (var a = 0; a <= id_agencias.length -1 ; a++)
    {
      for (var p = 0; p <= id_productos.length -1 ; p++)
      {
        datos_arreglo = [0,0,0,0,0,0,0,0,0,0,0,0];
        var verificar_ingreso = 0;
        for(var d=0; d<=responseData['dataset'][a]['data'].length-1 ;d++ )
        {
          if(id_productos[p] == parseInt(responseData['dataset'][a]['data'][d]['value']['id_productos_id']))
          {
            nombre_agencia = responseData['dataset'][a]['seriesname'] + " " + responseData['dataset'][a]['data'][d]['value']['id_productos_id__pro_nombre'];
            stack_ID_agencia = parseInt(responseData['dataset'][a]['data'][d]['value']['id_agencias_id']); 
            var mes = responseData['dataset'][a]['data'][d]['value']['tra_mes'];
            datos_arreglo[mes-1] = parseInt(responseData['dataset'][a]['data'][d]['value']['suma']);
           // console.log(datos_arreglo);
            verificar_ingreso = verificar_ingreso + 1;
          }
        }
        if(verificar_ingreso != 0){
        datos = {};
        datos['name'] = nombre_agencia;
        datos['data'] = datos_arreglo;
        datos['stack'] = stack_ID_agencia;
        series_datos.push(datos);
        }
      }
    }
    Highcharts.chart('container-barras-productos', {

    chart: {
        type: 'column'
    },

    title: {
        text: 'Total de ingresos por agencias, agrupados por productos'
    },

    xAxis: {
        categories: [
            'Ene',
            'Feb',
            'Mar',
            'Abr',
            'May',
            'Jun',
            'Jul',
            'Ago',
            'Sep',
            'Oct',
            'Nov',
            'Dec'
        ],
      //max:11
    },

    yAxis: {
        allowDecimals: false,
        min: 0,
        title: {
            text: 'Ingresos $'
        }
    },

    tooltip: {
        formatter: function () {
            return '<b>' + this.x + '</b><br/>' +
                this.series.name + ': ' + this.y + '<br/>' +
                'Total: ' + this.point.stackTotal;
        }
    },

    plotOptions: {
        column: {
            stacking: 'normal'
        }
    },

    series: series_datos
});
   }

function fusionLinesGeneral(responseData)
   {
    var series_datos = [];
    var datos = {};
    for (var i =0 ; i<=responseData['dataset'].length-1 ;i++)
    {
        datos = {};
        datos['name'] = responseData['dataset'][i]['seriesname'];
        datos['data'] = [];
        for(var d=0; d<=responseData['dataset'][i]['data'].length-1 ;d++ ){
             datos['data'].push(parseInt(responseData['dataset'][i]['data'][d]['value']));
          }
      series_datos.push(datos); 
    }
    Highcharts.chart('container-lines-general', {
    chart: {
        type: 'spline'
    },
    title: {
        text: 'Productividad Anual de los Asesores'
    },
    subtitle: {
        text: ''
    },
    xAxis: {
        categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    },
    yAxis: {
        title: {
            text: 'Ingresos'
        },
        labels: {
            formatter: function () {
                return '$ ' + this.value;
            }
        }
    },
    tooltip: {
        crosshairs: true,
        shared: true
    },
    plotOptions: {
        spline: {
            marker: {
                radius: 4,
                lineColor: '#666666',
                lineWidth: 1
            }
        }
    },
    series: series_datos
});
   } 
 


 



  