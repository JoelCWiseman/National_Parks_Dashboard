// app.js (formerly dashboard.js)
// Fetch the API key from the config.js file
// Make sure the config.js file is loaded before this script
const scriptTag = document.querySelector('script[src*="app.js"]');
const pathArray = scriptTag.src.split('/');
const configPath = pathArray.slice(0, pathArray.length - 1).join('/');
const script = document.createElement('script');
script.src = `${configPath}/config.js`;
document.head.appendChild(script);

// Function to fetch data from the Flask API
function fetchData(url) {
  return fetch(url)
    .then((response) => response.json())
    .catch((error) => {
      console.error("Error fetching data:", error);
    });
}

// Update the URLs to use the Flask API endpoints
const PARKS_API_URL = "http://localhost:5000/api/parks";
// ... other URLs for activities and amenities if needed

// Function to build the metadata panel (Park Info)
function buildParkInfo(parkCode) {
  const url = `${PARKS_API_URL}?parkCode=${parkCode}`;
  fetchData(url).then((data) => {
    // Code to handle the data and build the Park Info panel
  });
}

// Function to fetch and display the activities list for the selected National Park
function buildActivitiesList(parkCode) {
  const url = `${ACTIVITIES_API_URL}?parkCode=${parkCode}`;
  fetchData(url).then((data) => {
    // Code to handle the data and build the Activities list
  });
}

// Function to fetch and display the amenities list for the selected National Park
function buildAmenitiesList(parkCode) {
  const url = `${AMENITIES_API_URL}?parkCode=${parkCode}`;
  fetchData(url).then((data) => {
    // Code to handle the data and build the Amenities list
  });
}

// Function to initialize the dashboard
function init() {
  // Grab a reference to the dropdown select element
  let selector = d3.select("#selDataset");

  // Use fetch() to fetch the data from the parks API
  fetch(PARKS_API_URL)
    .then((response) => response.json())
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

// Function to handle a change in the dropdown selection
function optionChanged(newParkCode) {
  // Fetch new data each time a new park is selected
  buildParkInfo(newParkCode);
  buildActivitiesList(newParkCode);
  buildAmenitiesList(newParkCode);
}

// Initialize the dashboard
init();
