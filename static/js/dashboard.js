// Fetch the API key from the config.js file
// Make sure the config.js file is loaded before this script
const scriptTag = document.querySelector('script[src*="app.js"]');
const pathArray = scriptTag.src.split('/');
const configPath = pathArray.slice(0, pathArray.length - 1).join('/');
const script = document.createElement('script');
script.src = `${configPath}/config.js`;
document.head.appendChild(script);

// Function to fetch data from the API with the API key in the headers
function fetchDataWithApiKey(url) {
  return fetch(url, {
    headers: {
      "X-Api-Key": API_KEY,
    },
  })
    .then((response) => response.json())
    .catch((error) => {
      console.error("Error fetching data:", error);
    });
}

// Update the URLs to use the provided APIs
const PARKS_API_URL = "https://developer.nps.gov/api/v1/parks";
const ACTIVITIES_API_URL = "https://developer.nps.gov/api/v1/activities/parks";
const AMENITIES_API_URL = "https://developer.nps.gov/api/v1/amenities";

// Function to build the metadata panel (Park Info)
function buildParkInfo(parkCode) {
  const url = `${PARKS_API_URL}?api_key=${API_KEY}&parkCode=${parkCode}`;
  fetchDataWithApiKey(url).then((data) => {
    // Code to handle the data and build the Park Info panel
  });
}

// Function to fetch and display the activities list for the selected National Park
function buildActivitiesList(parkCode) {
  const url = `${ACTIVITIES_API_URL}?api_key=${API_KEY}&parkCode=${parkCode}`;
  fetchDataWithApiKey(url).then((data) => {
    // Code to handle the data and build the Activities list
  });
}

// Function to fetch and display the amenities list for the selected National Park
function buildAmenitiesList(parkCode) {
  const url = `${AMENITIES_API_URL}?api_key=${API_KEY}&parkCode=${parkCode}`;
  fetchDataWithApiKey(url).then((data) => {
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
