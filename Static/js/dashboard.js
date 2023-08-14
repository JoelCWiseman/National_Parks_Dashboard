const PARKS_API_URL = "/api/parks";



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

// Function to fetch topics data
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

      console.log(data);

      // Clear existing topics list
      topicsList.innerHTML = "";

      const topicsData = data.data;

      // Create a table element
      const table = document.createElement('table');
      table.className = "table table-bordered";

      // Determine the number of rows needed
      const numRows = Math.ceil(topicsData.length / 2);

      for (let rowIndex = 0; rowIndex < numRows; rowIndex++) {
        const row = document.createElement('tr');

        // Calculate indices for the two cells in the row
        const index1 = rowIndex * 2;
        const index2 = index1 + 1;

        // Create cell 1 (column 0)
        if (index1 < topicsData.length) {
          const cell1 = document.createElement('td');
          cell1.textContent = topicsData[index1].name;
          cell1.style.backgroundColor = rowIndex % 2 === 0 ? "lightblue" : "transparent";
          row.appendChild(cell1);
        }

        // Create cell 2 (column 1)
        if (index2 < topicsData.length) {
          const cell2 = document.createElement('td');
          cell2.textContent = topicsData[index2].name;
          cell2.style.backgroundColor = rowIndex % 2 === 0 ? "transparent" : "lightblue";
          row.appendChild(cell2);
        }

        table.appendChild(row);
      }

      // Append the table to the topicsList element
      topicsList.appendChild(table);
    })
    .catch(error => {
      console.error('Error fetching topics data:', error);
    });
}

  
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
      buildStateBarChart(firstParkCode);
      fetchTopics(firstParkCode);
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
  buildStateBarChart(newParkCode);
  fetchTopics(newParkCode);
}; 

// Initialize the dashboard
init();
