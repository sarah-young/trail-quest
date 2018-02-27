// <span id="trek_length"></span>
// <span id="radius"></span>

let slider1 = document.getElementById("radius-selection");
let output1 = document.getElementById("radius");
output1.innerHTML = slider1.value; // Display the default slider value

// Update the current slider value (each time you drag the slider handle)
slider1.oninput = function() {
    output1.innerHTML = this.value;
} //end of slider value <span> number for radius slidecontainer

let slider2 = document.getElementById("trek_length_selection");
let output2 = document.getElementById("trek_length");
output2.innerHTML = slider2.value; // Display the default slider value

// Update the current slider value (each time you drag the slider handle)
slider2.oninput = function() {
    output2.innerHTML = this.value;
} //end of slider value <span> number for trail length
// REFERENCE: https://www.w3schools.com/howto/howto_js_rangeslider.asp

$(document).on('click', '#getdirxns', getDirxns);

$(document).on('click', '#chosentrek', getTrek);
// Because button does not exist when the page loads!!!

$('#asynchronousClick').on('click', getTrails); // Trail Selector
// When button clicked, trail selected and more information displayed.

function getTrek(evt) {
  console.log("***In getTrek function!***");
  console.log($('#chosentrek').data('trailId'));
  $.post('/trek', {'chosentrail' : $('#chosentrek').data('trailId')}, function(result) {
      console.log(result);
      showTrek(result);
    })
  // $.ajax({
  //   url: "/trek",
  //   type: "POST",
  //   data: JSON.stringify({'chosentrail' : $('#chosentrek').data('trailId')}),
  //   processData: false,
  //   cache: true,
  //   success: function(result) {
  //     console.log(result);
  //     showTrek(result);
  //   }, //end of sucess input
  //   error: function(error) {
  //     console.log(error);
  //   } //end of error input
  // }); //end of AJAX element
} //end of getTrek function

function getTrails(evt) {
			$.ajax({
				url: "/trails_asychronous",
				type: "POST",
				data: $('#trailSelector').serialize(),
				processData: false,
				cache: true,
				success: function(response) {
					if (response === "FOO") {
						console.log('COORDINATES ERROR');
						let noCoordinates = document.getElementById("map");
						noCoordinates.innerHTML = "Hmm, no trails were found. Please check that the location is correct & in the United States."
					}
					else if (response === "BAR") {
						console.log('RANGE OR LOCATION ERROR');
						let noTrails = document.getElementById("map");
						noTrails.innerHTML = "Hmm, there aren't too many trails in this area. Maybe try a larger radius or different city in the United States?"; // Display the default slider value
					}
          else if (response === "FIZZ") {
            console.log('MISSING CITY SEARCH ERROR');
            let noCity = document.getElementById("map");
            noCity.innerHTML = "Please enter a City & State to begin your search."
          }

					else {
						initMap(response);
					}
					// Calling initMap function to display Google Map
				}, // end of response function

			  error: function(error) {
					console.log(error);
			  } // end of error handling function
			 }); // end of AJAX deets section
		}; //end of function getTrails


function initMap2(input) {
  console.log(input);

  let trailheadLat = input[0][0];
  let trailheadLong = input[0][1];

  let infoWindow = new google.maps.InfoWindow({
    width: 150
  });
  let html;
  let location = {lat: trailheadLat, lng: trailheadLong};
  let map = new google.maps.Map(document.getElementById('map'), {
    zoom: 20,
    center: location,
    mapTypeId: 'satellite'
    // mapTypeId: 'terrain'
  }); // end of jQuery statement

  // let marker = new google.maps.Marker({ //NOTE: Leaving this out for now. Only trailheadMarker is needed at this time.
  //   position: location,
  //   map: map
  // }); // end of marker statement
    // markerPlacement(input); NOTE: Does not seem to be needed.
  let trailheadMarker; // adding marker as a variable in the namespace
  trailheadMarker = new google.maps.Marker({
  position: new google.maps.LatLng(trailheadLat, trailheadLong),
  map: map,
  title: 'Selected Trek',
  icon: '/static/img/hikingIcon.png',
  animation: google.maps.Animation.DROP,
  });
    // TODO: mock input, and then maybe test to see if the input name (i.e. input[j].name ) is in the text
  html = ('<div class="window-content">' + '<br>' +
  '<p><b>Trail name: </b>' + input[0][2] + '</p>' + '<p><b>Trail length: </b>'
  + input[0][3] + '<b> Trail Difficulty:  </b>' + input[0][5] + '</p><p>' +
  '<p><b>Trail description: </b>' + input[0][6] + '</p>'
  + '<p> Starting Address: <input type="text" name="startingaddress" id="startingaddress" required><button type="button" id="getdirxns" name="getdirxns"'
  +'>Get Directions</button >' + '<input type="hidden" name="trailhead_coordinates" id="trailhead_coordinates" value="' + input[0][0]+input[0][1] + '">' +'</div>');
// TODO: Add button to get dirxns for trail


  bindInfoWindow(trailheadMarker, map, infoWindow, html);
  toggleBounce(trailheadMarker);
} //end of initMap2 function



function initMap(input) {
		let trailLong = input[0].city_long;
		let trailLat = input[0].city_lat;
		let infoWindow = new google.maps.InfoWindow({
        width: 150
		});
		let html;
	  let location = {lat: trailLat, lng: trailLong}; //latitude and longitude for city
	  let map = new google.maps.Map(document.getElementById('map'), {
	    zoom: 10,
	    center: location,
      mapTypeId: 'satellite'
		}); // end of jQuery statement

	  let marker = new google.maps.Marker({
	    position: location,
	    map: map
		}); // end of marker statement
			// markerPlacement(input);
		let trailMarker; // adding marker as a variable in the namespace

		for (let j = 0; j < input.length; j += 1) {
			trailMarker = new google.maps.Marker({
			position: new google.maps.LatLng(input[j].latitude, input[j].longitude),
			map: map,
			title: 'Trail: ' + input[j].name,
			icon: '/static/img/hikingIcon.png',
			animation: google.maps.Animation.DROP,
			});
			// TODO: mock input, and then maybe test to see if the input name (i.e. input[j].name ) is in the text
			html = ('<div class="window-content">' + '<br>' +
              '<p><b>Trail name: </b>' + input[j].name + '</p>' + '<p>' +
              '<p><b>Trail description: </b>' + input[j].summary + '</p>' + '<p>' +
              '<p><b>Trail length: </b>' + input[j].length +'</p><p>'+
              '<button type="button" id="chosentrek" name="chosentrek" data-trail-id='
              + input[j].id +'>Add trail to My Trails</button >' + '</div>');
			bindInfoWindow(trailMarker, map, infoWindow, html);
		} // end of trailMarker for loop
		// let circle = new google.maps.Circle({ // circle for user chosen radius on map
		// 	map: map,
		// 	radius: input[0].radius_in_meters,
		// 	fillColor: '#b394d1',
		// 	strokeWeight: .1
		// }); // end of circle statement
		// circle.bindTo('center', marker, 'position');
		drop(input);
		toggleBounce(trailMarker);
} //end of initMap function

function drop(input) { //marker animation for REASONS
  for (let k = 0; k < input.length; k++) {
    setTimeout(function() {
    }, k * 200);
  }
} //end of drop function

function toggleBounce(trailMarker) { //cute BOUNCE when markers drop <3
	if (trailMarker.getAnimation() !== null) {
		trailMarker.setAnimation(null);
	} //end of if
	else {
		trailMarker.setAnimation(google.maps.Animation.BOUNCE);
	} //end of else
} //end of toggleBounce function

function bindInfoWindow(trailMarker, map, infoWindow, html) {
        google.maps.event.addListener(trailMarker, 'click', function () {
            infoWindow.close();
            infoWindow.setContent(html);
            infoWindow.open(map, trailMarker);
        });
} //end of bindInfoWindow function

function showTrek(result) {
  console.log('IN SHOWTREK FUNCTION!');
	console.log(result);

  let trek_lat, trek_long;
  trek_lat = result[0];
  trek_long = result[1];
  initMap2(result);


} // end of showTrek function

function getDirxns() {
  console.log("getdirxns button working!!!");
  if (document.getElementById("startingaddress").value === "") {
    alert("Please enter a valid address.");
    console.log('In alert function');
  } // end of if statement
  else {
    $.post('/dirxns', {'startingaddress' : $('#startingaddress').value, 'trailhead_coordinates': $('#trailhead_coordinates').value }, function(result) {
      console.log(result);
      // TODO: put results in a function!
      })

  } //end of else statement


} // end of getDirxns function

	// =
	// (("Trail Name: " + trailName + "<br>" + trailDifficulty + "<br>" + trailLength + "<br>" +
	// 	trailDetails + "<br>" + "<img src=" + trailPicture+ ">"))
	// 	// look at trek info in server.py
