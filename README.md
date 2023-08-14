# National_Parks_Dashboard
## The goal of this repository is to show some of the data from NPS APIs in different visualizations. 

We began with a simple folder structure so everything could work together. We have the python files and the filled sqlite files not in folders. We have a Static folder with the empty sqlite files, a CSS folder with the style.css and a JS folder with the javascript files. We have a template folder for the index.html file. Next we looked through the api documentation from the NPS and decided where to pull data from and what data we wanted. We wanted the base API url for the parks and then we pulled other APIs from there. 

There was a lot of trial and error when finding the correct data. Some of the ideas we had couldn't be supported by the data because it wasn't available. We experimented with the activities, amentities, events, and campgrounds of the parks. We ended up using geographical information and information about topics from each park. All this information is in the api_pull_v2 and we tracked errors in an api.log file. 

Once we got all the data, we made an app.py to get the routes we needed with Flask and the api pulls. We also made a html file to make all the containers and text for our webpage. The dashboard.js is the main file that makes the html file work. The webpage runs from the app.py file when you run it through flask. 

In the dashboard, we make the dropdown menu have all the parks and it shows the park code and coordinate when you change parks. We have a map of the US that has circles for each park and when you click on a circle there is the park name, coordinates and a link to open it in google maps. We used plotly to make a charts and we made a bar chart of the amount of parks in each state. To achieve this we made an array from the information in the api pulls and built the bart chart this way. We also made a table of all the topics related to the national parks. 

To introduce a new javascript library, we used elevator.js. When you scroll to the bottom of the page, if you click back to top it'll autoscroll back up. This library contains music as well, but we didn't include it. We thought it fit well because there is scrolling with the map and the "back to top" button can get you to the dropdown menu. We used other libraries like leaflet (for the map), bootstrap, and D3. 
