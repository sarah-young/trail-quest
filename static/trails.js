  // Google Map centered on lat/long for city selected
  function initMap() {

      console.log('here');
      var location = {lat: {{ city_latitude|safe }}, lng: {{ city_longitude|safe }} }; //latitude and longitude for city
      console.log(location);

      var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 10,
        center: location
      });


      var marker = new google.maps.Marker({
        position: location,
        map: map
      });


      var trailsJSON = {{ selected_trails|tojson }}; //converting python list to js array!
      console.log(trailsJSON);
      

      let trailMarker, html; // adding marker as a variable in the namespace 


      for (let i = 0; i < trailsJSON.length; i += 1) {
        console.log(trailsJSON[i]);

        trailMarker = new google.maps.Marker({
          position: new google.maps.LatLng(trailsJSON[i].latitude, trailsJSON[i].longitude),
          map: map,
          title: 'Trail: ' + trailsJSON[i].name,
          icon: '/static/img/hikingIcon.png'
        });
      }


      // Radius for user inputted distance
      var circle = new google.maps.Circle({
        map: map,
        radius: {{ radius }},    // 10 miles in metres // Make this dynamic so it links to the radius input by the user
        fillColor: '#b394d1',
        strokeWeight: .1
      });

        // Function for adorable marker drop :3
        function drop() {
          for (var i =0; i < markerArray.length; i++) {
            setTimeout(function() {
              addMarkerMethod();
            }, i * 200);
          }
        }
        circle.bindTo('center', marker, 'position');
      };

        // Function to add 'bounce' to markers

        function toggleBounce() {
          if (marker.getAnimation() !== null) {
            marker.setAnimation(null);
          } else {
            marker.setAnimation(google.maps.Animation.BOUNCE);
          }
        };
