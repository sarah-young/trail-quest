// JavaScript elements for homepage.html

// Slider bars for radius & length of hike
console.log(document.getElementById("trek_length"));
					var slider1 = document.getElementById("radius-selection");
					var output1 = document.getElementById("radius");
					output1.innerHTML = slider1.value; // Display the default slider value

					// Update the current slider value (each time you drag the slider handle)
					slider1.oninput = function() {
					    output1.innerHTML = this.value;
					    						}
var slider2 = document.getElementById("trek_length_selection");

var output2 = document.getElementById("trek_length");
output2.innerHTML = slider2.value; // Display the default slider value

// Update the current slider value (each time you drag the slider handle)
slider2.oninput = function() {
	output2.innerHTML = this.value;
}



//Creating asynchronous call for form #yay
document.getElementById("asynchrousClick").addEventListener("click", function() {
	let formData = new FormData(document.getElementById('trailSelector'));
	console.log(formData);
	$.ajax({
		url: "/trails_asychronous",
		type: "GET",
		data: formData,
		processData: false,
		cache: false,
		success: function(response){
			var k=response;
			console.log(`Response: `, response)
			let trailDetails, trailName, trailPicture, trailLength, trailDifficulty;

			for (let i = 0; i < k.length; i += 1) {
		    	trailName = k[i].name
		    	console.log(trailName);
		    	trailDetails = k[i].summary
		    	console.log(trailDetails);
		    	trailPicture = k[i].imgSmall
		    	console.log(trailPicture);
		    	trailLength = k[i].length
		    	console.log(trailLength);
		    	trailDifficulty = k[i].difficulty
		    	console.log(trailDifficulty);	

		    	document.getElementById("selectedtrails1").innerHTML = trailName + "<br>" + trailDifficulty + "<br>" + trailLength + "<br>" + trailDetails + "<br>" + "<img src=" + trailPicture + ">";
		    	};
			}
		})
	});

// 