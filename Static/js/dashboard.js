const PARKS_API_URL = "/api/parks";

//ScrollReveal().reveal('.container');

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
  // fetchData(`${PARKS_API_URL}/${parkCode}`)
  fetchData(`${PARKS_API_URL}`)
    .then((data) => {
      
      let choice = d3.select('select').node().value;
      let park = data.data.filter(obj=> obj.parkCode == choice)[0];

      console.log(park);
      const infoContainer = d3.select("#park-info");
      infoContainer.html("");
      infoContainer.append("h3").text(park.fullName);
      infoContainer.append("p").text(`State: ${park.stateCode}`);
      infoContainer.append("p").text(`Latitude: ${park.latitude}`);
      infoContainer.append("p").text(`Longitude: ${park.longitude}`);
    });
}

/*// Function to build campground info chart
function buildCampgroundChart(parkCode) {
  fetchData(`${PARKS_API_URL}/${parkCode}/campgrounds`)
    .then((data) => {
      const campgrounds = data.data;
	  
	  let topCampgrounds = campgrounds
        .sort((a, b) => b.occupancy - a.occupancy)
        .slice(0, 10);

      let campgroundNames = topCampgrounds.map(campground => campground.name);
      let campgroundOccupancies = topCampgrounds.map(campground => campground.occupancy);

      // Create the trace for the campground bar chart
      let barTrace = {
        x: campgroundOccupancies,
        y: campgroundNames,
        text: campgroundNames,
        type: "bar",
        orientation: "h"
      };

      let barData = [barTrace];

      let barLayout = {
        title: `Campground information`,
        margin: { t: 30, l: 150 }
      };

      // Update the campground chart container
      let chartContainer = d3.select("#campground-chart");
      chartContainer.html(""); // Clear existing chart
      chartContainer.append("div").attr("id", "campground-bar-chart");

      Plotly.newPlot("campground-bar-chart", barData, barLayout);
    });
} */

/*// Function to fetch topics data
function fetchTopics() {
  return fetch('/api/get_topics')
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      const topicsList = document.getElementById('topicsList');

      // Populate the topics list
      data.data.forEach(topic => {
        const listItem = document.createElement('div');
        listItem.textContent = topic.name;
        topicsList.appendChild(listItem);
      });
    })
    .catch(error => {
      console.error('Error fetching topics data:', error);
    });
}*/

// Function to make all states bar chart
function buildAllStateBarChart(parkCode) {
  fetchData(`${PARKS_API_URL}`)
    .then((data) => {
      //this is one way to make the chart where it's all the states at with each dropdown change
      let selectedParkCode = d3.select('select').node().value;
      let park = data.data.filter(obj => obj.parkCode == selectedParkCode[0]);

      if (!park) {
        console.error('Park not found for the given code');
        return;
      }

      let { stateCode } = park;

      parkNumber = stateData.map(function (row){
        return row.amountOfParks
      });
      stateNumber = stateData.map(function (row){
        return row.State
      });
      
      var stateAllBarChart = {
        x: parkNumber,
        y: stateNumber,
        type: 'bar',
        orientation: 'h'
      };
      
      var data = [stateAllBarChart];

      var layout = {
        xaxis: {
           range: [0, 40],
          title: 'Number of Parks per State'
        },
        yaxis: {
           ype: 'category',
          title: 'States',
        }
      };

      // Update the bar chart container
      //let barContainer = d3.select("#bar");
      //barContainer.html(""); // Clear existing chart
      //barContainer.append("div").attr("id", "bar");

      // Clear the existing chart
      const scatterContainer = d3.select("#b");
      scatterContainer.selectAll("*").remove();
      
      Plotly.newPlot('topicsList', data, layout);
    });
    //.catch((error) => {
      //console.error('Error fetching data:', error);
    //});
};
  
// Function to make each state bar chart
function buildStateBarChart(parkCode) {
  fetchData(`${PARKS_API_URL}`)
    .then((data) => {

	//This the another way where the chart will change with the dropdown for the state that is with that park
      let selectedParkCode = d3.select('select').node().value;
      let park = data.data.find(obj => obj.parkCode == selectedParkCode);

      if (!park) {
        console.error('Park not found for the given code');
        return;
      }

      let { stateCode } = park;

      parkNumber = stateData.map(function (row){
        return row.amountOfParks
      });
      
      var stateBarChart = {
        x: parkNumber,
        y: [stateCode],
        type: 'bar',
        orientation: 'h'
      };
      
      var data = [stateBarChart];

      var layout = {
        xaxis: {
           range: [0, 40],
          title: 'Number of Parks per State'
        },
        yaxis: {
           ype: 'category',
          title: 'States',
        }
      };

      // Update the bar chart container
      //let barContainer = d3.select("#bar");
      //barContainer.html(""); // Clear existing chart
      //barContainer.append("div").attr("id", "bar");

      // Clear the existing chart
      const scatterContainer = d3.select("#b");
      scatterContainer.selectAll("*").remove();
      
      Plotly.newPlot('barState', data, layout);
    });
    //.catch((error) => {
      //console.error('Error fetching data:', error);
    //});
}; 

/*/ Function to build the activities list
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
} */

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
      //buildActivitiesList(firstParkCode);
      //buildAmenitiesList(firstParkCode);
	    //buildCampgroundChart(firstParkCode);
      buildStateBarChart(firstParkCode);
      buildAllStateBarChart(firstParkCode);
    });
}

// Function to initialize the interactive map
function initMap(parks) {
  let map = L.map('map').setView([45.8283, -98.5795], 4); // Set initial map view to the USA

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { 
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(map);

 

  // Add markers for each park
  parks.forEach(park => {
    const marker = L.circleMarker([park.latitude, park.longitude]).addTo(map);
    const googleMapsLink = `https://www.google.com/maps?q=${park.latitude},${park.longitude}`;
    marker.bindPopup(`<b>${park.fullName}</b><br>Latitude: ${park.latitude}<br>Longitude: ${park.longitude}<br><a href="${googleMapsLink}" target="_blank">Open in Google Maps</a>`);
});
}

// Fetch park data and initialize the map
fetchData(PARKS_API_URL)
  .then(data => {
    const parks = data.data;
    console.log(data.data)
    initMap(parks);
  }); 
//Function to handle a change in the dropdown selection
function optionChanged(newParkCode) {
  // Fetch new data each time a new park is selected
  buildParkInfo(newParkCode);
  //buildActivitiesList(newParkCode);
  //buildAmenitiesList(newParkCode);
  //buildCampgroundChart(newParkCode);
  buildStateBarChart(newParkCode);
  buildAllStateBarChart(newParkCode);
}; 

// Initialize the dashboard
init();
