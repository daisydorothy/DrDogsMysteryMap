
var markers = [];
var gameStats = {score: 0, round: 0, meanScore:0}
var currentScene = null

//document.getElementById("play_again").hidden = true; todo: hide until next round

function initialize(){
  document.getElementById("guessButton").disabled = true;
  $("#guessResults").hide();
  guessMap = makeGuessMap();
  makeGuessMapClickable(guessMap);

  // set up current streetview round
  currentScene = getLocation();
  makeStreetview();

}

function getLocation(){
  var locales = []
  // make an array of dicts from city-list
  city_list = city_list.slice(1) // get rid of headings lol
  for (i = 0; i < city_list.length; i++){
    var city_entry = {}
    city_entry.name = city_list[i][2]
    city_entry.country = city_list[i][3]
    city_entry.position = {lat:Number(city_list[i][0]), lng:Number(city_list[i][1])}
    locales.push(city_entry)
  }

  locales = _.shuffle(locales)
  currentScene = locales.pop();
  return currentScene
}

function makeGuessMap(){
  // create guess map - world map user will place their guess on
  var guessMap = new google.maps.Map(document.getElementById("guessMap"), {
    center: { lat: 51.482578, lng: -0.007659 }, // centered at Greenwich
    zoom: 1,
    mapTypeId: "roadmap",
    streetViewControl: false,
    mapId: "guessMap", // Map ID is required for advanced markers.
  });
  return guessMap;
}

function makeGuessMapClickable(guessMap){
  guessMap.addListener("click", (e) => {
    placeMarkerAndPanTo(e.latLng, guessMap);
  });
}


// plot user's guess
function placeMarkerAndPanTo(latLng, guessMap) {
  // clear old marker if made a previous guess
  if (markers.length > 0){
    markers[0].setMap(null)
    markers = []
  }

  // create a new marker
  const marker = new google.maps.Marker({
    position: latLng,
    map: guessMap,
    title: "guess",
  });
  markers.push(marker);

  document.getElementById("guessButton").disabled = false; // allow user to guess now
  guessMap.panTo(latLng); // pan to selected area
}


function makeStreetview(){
  var panorama = new google.maps.StreetViewPanorama(
    document.getElementById("pano"),
    {
      position: currentScene["position"],
      addressControl: false,
      panControl: false,
      showRoadLabels: false,
      pov: {
        heading: 34,
        pitch: 10,
      },
    }
  );
}



function makeGuess(){
  distKM = calculateDistance();
  updateGuessMap(guessMap);
  updateStats(distKM);
  updateTxtDisplay(distKM);

  // misc UX stuff
  google.maps.event.clearListeners(guessMap, 'click'); // stop placing new markers
  document.getElementById("guessButton").disabled = true;
  $("#playAgain").show();
}


function calculateDistance(){
  // calculate distance in meters
  var distKM = google.maps.geometry.spherical.computeDistanceBetween(markers[0].getPosition(), currentScene["position"])
  distKM = Math.round(distKM/1000)
  return distKM
}


function updateGuessMap(guessMap){
  // add marker
  guessMap.setCenter(currentScene["position"]) // to change!

  const marker = new google.maps.Marker({
    position: currentScene["position"],
    map: guessMap,
  });

  // set flightpath coords
  const pathCoords = [
    currentScene["position"],
    markers[0].getPosition(),
  ];
  // create flightPath
  const flightPath = new google.maps.Polyline({
    path: pathCoords,
    geodesic: false,
    strokeColor: "#FF0000",
    strokeOpacity: 1.0,
    strokeWeight: 4,
  });
  flightPath.setMap(guessMap);
}

function updateStats(distKM){
  gameStats["score"] = gameStats["score"] += distKM
  gameStats["round"] = gameStats["round"] +=1
  gameStats["meanScore"] = gameStats["score"] / gameStats["round"]
  // maybe do something more with scores/rounds if i were to ever develop the gameplay
  // for now keep it simple - just report average guess
}

function updateTxtDisplay(distKM){
  document.getElementById("correctLoc").innerHTML = "Real location was " + currentScene["name"] + ', ' + currentScene["country"];
  document.getElementById("distance").innerHTML = "Your guess was off by " + distKM + " km";
  document.getElementById("meanScore").innerHTML = "On average, your guesses are " + gameStats["meanScore"]+ 'km off';
  // show it
  $("#guessResults").show();
}
