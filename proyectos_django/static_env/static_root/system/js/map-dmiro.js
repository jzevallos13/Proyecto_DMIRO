var marker = null;
var id_agencia = 0;
var jsonAgencias = $.getJSON("/app/api/mapAgencias");


function initMap() {
    var marcadores = [];
    var datos = [];
    jsonAgencias.done(function(data){
      for (i in data['agencias']){
        var nombre = data['agencias'][i]['age_nombre'];
        var direccion = data['agencias'][i]['age_direccion'];
        var coordenadax = data['agencias'][i]['age_coordenadax'];
        var coordenaday = data['agencias'][i]['age_coordenaday'];
        datos = [nombre + " - " +direccion, coordenadax, coordenaday];
        marcadores.push(datos);
      }
    });
    console.log(marcadores);
    var mapOptions = {
      center: new google.maps.LatLng(-2.1100639, -79.9557909),
      zoom: 8,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    var map = new google.maps.Map(document.getElementById("mapa"),
        mapOptions);
       var infowindow = new google.maps.InfoWindow();
    var marker, i;
    for (i = 0; i < marcadores.length; i++) {  
        marker = new google.maps.Marker({
        position: new google.maps.LatLng(marcadores[i][1], marcadores[i][2]),
        map: map
      });
      google.maps.event.addListener(marker, 'click', (function(marker, i) {return function() {
        infowindow.setContent(marcadores[i][0]);
            infowindow.open(map, marker);    
      jsonAgencias.done(function(data){
      for (i in data['agencias']){
        var id = data['agencias'][i]['id'];
        var nombre = data['agencias'][i]['age_nombre'];
        var coordenadax = data['agencias'][i]['age_coordenadax'];
        if ((marker.position.lat() == coordenadax)){
                id_agencia = id;
                document.getElementById('chart-container-lines').innerHTML='';
                document.getElementById('chart-container-circular').innerHTML='';
                document.getElementById('selecionar-agencia').innerHTML='Agencia';
                document.getElementById('agencia-seleccionada').innerHTML=nombre;
                document.getElementById('selectAnio').selectedIndex = 0;
           }
          }
        });	
          } 
        })(marker, i));
      } 
   
    }

  function myFunction() {
    anio = $("#selectAnio").val();
    if ((anio != 0) && (id_agencia != 0)){
      document.getElementById('chart-container-lines').innerHTML='';
      document.getElementById('chart-container-circular').innerHTML='';
      var json = $.getJSON("/app/api/fusionLines/"+id_agencia+"/"+anio+"/");
      json.done(function(data){
        if(data['dataset'] == ''){
          document.getElementById('chart-container-lines').innerHTML='';
          document.getElementById('chart-container-circular').innerHTML='';
        }
        else{fusionLines(data);}
      });
    }
    else{
      document.getElementById('chart-container-lines').innerHTML='';
      document.getElementById('chart-container-circular').innerHTML='';
    }
}

       //Funcion Cargar Datos fusionBarras
   function fusionLines(responseData){
      FusionCharts.ready(function () 
      {
          var revenueChart = new FusionCharts(
          {
            type: 'msline',
            renderAt: 'chart-container-lines',
            width: '475',
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
    //}
   }
  //FIN
  //Funcion Cargar Datos fusionCircular
   function fusionCircular(responseData)
   {
    var mes = 0;
    lista_meses = ["Ene", "Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"];
    lista_meses.forEach(function(elemento, valor){
      if(responseData['categoryLabel'] == elemento){
        mes = valor + 1;
      }
    })
    //console.log(responseData); 
  //console.log(responseData['datasetName']);
    var cadena_asesor = String([responseData['datasetName']]);
    var split_cadena = cadena_asesor.split(",")[0];
    var split_spit_cadena = String(split_cadena);
    var split_split_spit_cadena = split_spit_cadena.split(":"); 
    var id_asesor = parseInt(String(split_split_spit_cadena[1]));
    //console.log(id_asesor);
    FusionCharts.ready(function () 
    {
        $.getJSON("/app/api/fusionCircular/"+id_agencia+"/"+id_asesor+"/"+mes+"/", function(result)
        {
            var revenueChart = new FusionCharts(
            {
              type: 'doughnut2d',
              renderAt: 'chart-container-circular',
              width: '475',
              height: '350',
              dataFormat: 'json',
              dataSource: result
             }).render();
        });
      });
   }
   //FIN
   //Funcion Cargar Datos fusionBarras
   function fusionBarras(responseData){
      FusionCharts.ready(function () 
      {
          var revenueChart = new FusionCharts(
          {
            type: 'column2d',
            renderAt: 'chart-container',
            width: '475',
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
 



  