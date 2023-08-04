const PARKS_API_URL = "http://localhost:5000/api/parks";

// Function to fetch data from the Flask API
function fetchData(url) {
  return fetch(url)
    .then((response) => response.json())
    .catch((error) => {
      console.error("Error fetching data:", error);
    });
}

// Function to build the park info container
function buildParkInfo(parkCode) {
  fetchData(`${PARKS_API_URL}/${parkCode}`)
    .then((data) => {
      const park = data.data;
      const infoContainer = d3.select("#park-info");
      infoContainer.html("");
      infoContainer.append("h3").text(park.fullName);
      infoContainer.append("p").text(`State: ${park.stateCode}`);
      infoContainer.append("p").text(`Latitude: ${park.latitude}`);
      infoContainer.append("p").text(`Longitude: ${park.longitude}`);
    });
}

// Function to build the activities list
function buildActivitiesList(parkCode) {
  fetchData(`${PARKS_API_URL}/${parkCode}/activities`)
    .then((data) => {
      const activities = data.data;
      const activitiesList = d3.select("#activities-list");
      activitiesList.html("");
      activitiesList.append("h4").text("Activities Available:");
      const listItems = activities.map(activity => `<li>${activity}</li>`);
      activitiesList.append("ul").html(listItems.join(""));
    });
}

// Function to build the amenities list
function buildAmenitiesList(parkCode) {
  fetchData(`${PARKS_API_URL}/${parkCode}/amenities`)
    .then((data) => {
      const amenities = data.data;
      const amenitiesList = d3.select("#amenities-list");
      amenitiesList.html("");
      amenitiesList.append("h4").text("Amenities Available:");
      const listItems = amenities.map(amenity => `<li>${amenity}</li>`);
      amenitiesList.append("ul").html(listItems.join(""));
    });
}

// Function to initialize the dashboard
function init() {
  // Grab a reference to the dropdown select element
  let selector = d3.select("#selDataset");

  // Use fetch() to fetch the data from the parks API
  fetchData(PARKS_API_URL)
    .then((data) => {
      let parks = data.data;

      // Populate the dropdown options with the park names
      parks.forEach((park) => {
        selector.append("option")
          .text(park.fullName)
          .property("value", park.parkCode);
      });

      // Use the first park from the list to build the initial panels
      let firstParkCode = parks[0].parkCode;
      buildParkInfo(firstParkCode);
      buildActivitiesList(firstParkCode);
      buildAmenitiesList(firstParkCode);
    });
}

// Function to initialize the interactive map
function initMap(parks) {
  const map = L.map('map').setView([39.8283, -98.5795], 4); // Set initial map view to the USA

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(map);

  // Add markers for each park
  parks.forEach(park => {
    const marker = L.circleMarker([park.latitude, park.longitude]).addTo(map);
    marker.bindPopup(`<b>${park.fullName}</b><br>Latitude: ${park.latitude}<br>Longitude: ${park.longitude}`);
  });
}

// Fetch park data and initialize the map
fetchData(PARKS_API_URL)
  .then(data => {
    const parks = data.data;
    initMap(parks);
  });
// Function to handle a change in the dropdown selection
function optionChanged(newParkCode) {
  // Fetch new data each time a new park is selected
  buildParkInfo(newParkCode);
  buildActivitiesList(newParkCode);
  buildAmenitiesList(newParkCode);
}

// Initialize the dashboard
init();
