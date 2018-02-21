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



$('#asynchronousClick').on('click', getTrails);
// When button clicked, trail selected and more information displayed.

function getTrails(evt) {

		let data = {"city": document.getElementById("cityname"),
								"state": document.getElementById("statename"),
								"radius": document.getElementById("radius-selection"),
								"traillength": document.getElementById("trek_length_selection"),
								"traildifficulty": document.getElementById("traildifficulty")
		} // end of data object.

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
						noCoordinates.innerHTML = "Hmm, no trails were found. Please check that the location is correct & is in the United States."
					}
					else if (response === "BAR") {
						console.log('RANGE OR LOCATION ERROR');
						let noTrails = document.getElementById("map");
						noTrails.innerHTML = "Hmm, there aren't too many trails in this area. Maybe try a larger radius or different city in the United States?"; // Display the default slider value
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

function initMap(input) {
		console.log(input);
		console.log("MAP: here");
		let trailLong = input[0].city_long;
		let trailLat = input[0].city_lat;
		let infoWindow = new google.maps.InfoWindow({
        width: 150
		});
		let html;
		console.log(trailLong);
		console.log(trailLat);
		// lat and lng are not coming through as integers :(
	  let location = {lat: trailLat, lng: trailLong};
		//latitude and longitude for city
	  let map = new google.maps.Map(document.getElementById('map'), {
	    zoom: 8,
	    center: location
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
			html = ('<div class="window-content">' +
              '<img src="'+input[j].imgSmall+'" alt="trailimage" style="width:100%;" class="thumbnail">' +
              '<p><b>Trail name: </b>' + input[j].name + '</p>' + '<p>' + input[j].summary + '</p>' +
							'<p>'+ '<button type="button" id="chosentrail" name="'+ input[j].id + '">Add trail to My Trails</button>'
              + '</div>');
			bindInfoWindow(trailMarker, map, infoWindow, html);
		} // end of trailMarker for loop
		console.log('Here: radius');
		let circle = new google.maps.Circle({ // circle for user chosen radius on map
			map: map,
			radius: input[0].radius_in_meters,
			fillColor: '#b394d1',
			strokeWeight: .1
		}); // end of circle statement
		circle.bindTo('center', marker, 'position');
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

function bindInfoWindow(trailMarker, map, infoWindow, html) { //infoWindow for each trail; might do away with text outside this!
        google.maps.event.addListener(trailMarker, 'click', function () {
            infoWindow.close();
            infoWindow.setContent(html);
            infoWindow.open(map, trailMarker);
        });
} //end of bindInfoWindow function



// $('#chosentrail').on('click',getTrek);

// function getTrek(evt) {
//
// 	let data = {"trail_id":document.getElementByName("chosentrail")} //end of data
//
// 	$.ajax({
// 		url: "/trek",
// 		type: "POST",
// 		data: $('#chosentrail').serialize(),
// 		processData: false,
// 		cache: true,
// 		sucess: function(input) {
// 			console.log(input);
// 			showTrek(input);
// 		}, //end of sucess input
// 		error: function(error) {
// 			console.log(error);
// 		} //end of error input
// 	}); //end of AJAX element
// } //end of getTrek function

// function showTrek(input) {
//
// 	document.getElementById("trek").innerHTML =
// 	(("Testing"));
// }
//
// 	// =
// 	// (("Trail Name: " + trailName + "<br>" + trailDifficulty + "<br>" + trailLength + "<br>" +
// 	// 	trailDetails + "<br>" + "<img src=" + trailPicture+ ">"))
// 	// 	// look at trek info in server.py
// }
