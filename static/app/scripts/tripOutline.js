$(document).ready(function() {
    initMap();
});

function openTab(evt) {
    // Declare all variables
    var i, tabcontent, tablinks
    var tabName = document.getElementById('ddlOptions').value
    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for(i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Show the current tab
    document.getElementById(tabName).style.display = "block"

}

function geocodeAddress(resultsMap) {
    var geocoder = new google.maps.Geocoder();
    var address = document.getElementById('pac-input').value;
    geocoder.geocode({ 'address': address }, function (results, status) {
        if (status === 'OK') {
            // resultsMap.setCenter(results[0].geometry.location);
            var marker = new google.maps.Marker({
                map: resultsMap,
                position: results[0].geometry.location
            });
            // set the values in the form so it can be saved properly
            var formatted_address, name, lat, lng
            name = results[0].address_components[0].long_name
            formatted_address = results[0].formatted_address;
            lat = results[0].geometry.location.lat();
            lng = results[0].geometry.location.lng();

            document.getElementById('id_name').value = name
            document.getElementById('id_address').value = formatted_address
            document.getElementById('id_lat').value = lat.toFixed(6);
            document.getElementById('id_lng').value = lng.toFixed(6);
        } else {
            alert('Geocode was not successful for the following reason: ' + status);
        }
    });
}

function initMap() {
    // Create a new blank array for all the listings markers.
    var marker_objects = [];
    // Constructor creates a new map - only center and zoom are required.
   var map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: 41.157557, lng: -81.242047 }, // 41.157557,-81.242047
        zoom: 5,
        //mapTypeControl: false
   });
    // because apparently sending it with the escapejs wasn't enough
    // to use it right away have to parse the JSON data into a usable formate?!?! wtf
    // will do analysis late ron speed just out of pure curiousity
    // really starting to debate that whole is it worth the developement time to have figured this
    // out instead if doing infile js, especially if there is a significant (or even a not so significant) performance cost
    // alas it is done and I learned somethings if I ever DID need to do this
    // and thus ends my solilquiy, performance results to be posted later
    // est. time to implement this and get it working ~1.5 hours
    // pointsData = {};
    var pointsData = JSON.parse(points);

   for (var i = 0; i < pointsData.length ; i++) {

               var myLatLng = new google.maps.LatLng(pointsData[i].fields.lat, pointsData[i].fields.lng);
              // var content = 

               var markerColor = pointsData[i].fields.confirmed ? 'http://maps.google.com/mapfiles/ms/icons/green-dot.png' : 'http://maps.google.com/mapfiles/ms/icons/yellow-dot.png'

               marker = new google.maps.Marker({
                   position: myLatLng,
                   map: map,
                   title: pointsData[i].fields.name,
                  // label: pointsData[i].fields.orderVisiting,
                   icon: markerColor
               });

              // infowindow.setContent(content);
              //initInfoWindow(marker, infowindow);
               var infowindow = new google.maps.InfoWindow;
               google.maps.event.addListener(marker, "click", (function (marker, i) {
                   return function (evt) {
                       var content = '<h1 class="firstHeading">' + marker.title + '</h1> <br />' +
                                     '<h3 class="secondHeading">Est. Date: ' + pointsData[i].fields.date + '</h2><br />' +
                                     '<h3 class="secondHeading">The Plan</h2>' + '<p>' +
                                       pointsData[i].fields.description + '</p>';
                       infowindow.setContent(content);
                       infowindow.open(map, marker);
                   }
               })(marker, i));
               marker_objects.push(marker);
       } // end of points loop

    // Create the search box and link it to the UI element.
    var input = document.getElementById('pac-input');
    var searchBox = new google.maps.places.SearchBox(input);

    document.getElementById('submit').addEventListener('click', function() {
        geocodeAddress(map);
    });

    document.getElementById('#pac-input').addEventListener('onblur', function () {
        geocodeAddress(map);
    })


} // end of init map

// use this function tp setup the infowindow
function initInfoWindow(marker, infowindow) {

    google.maps.event.addEventListener(marker, 'click', function () {
        infowindow.open(map, this);
    })
}


    
