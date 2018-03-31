
var marker = null;
function initMap() {
    var marcadores = [
    ['Sushi Isao', -2.1752007, -79.90782109999998],
    ['Noe Sushi', -2.1751524, -79.92314199999998],
    ['Miyako', -2.1700195, -79.90900399999998],
    ['Nanosh', -2.1673177, -79.9147332]];
    var mapOptions = {
      center: new google.maps.LatLng(-2.1699498, -79.9230802),
      zoom: 14,
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
			if (marker.position.lat() == -2.1752007){
                var contenedor=document.getElementById("imagen");
                contenedor.src="sushi.jpg";
			}
			if (marker.position.lat() == -2.1751524){
                var contenedor=document.getElementById("imagen");
                contenedor.src="sushi1.jpg";
			}
			if (marker.position.lat() == -2.1700195){
                var contenedor=document.getElementById("imagen");
                contenedor.src="sushi2.jpg";
			}
			if (marker.position.lat() == -2.1673177){
                var contenedor=document.getElementById("imagen");
                contenedor.src="sushi3.jpg";
			}
        
          } 
        })(marker, i));
      } 
   
    }
    
 



  