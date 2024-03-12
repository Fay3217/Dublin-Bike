# Dublin Bike

## Introduction ##

Dublin Bikes is a web-application software which will provide relevant information regarding Dublin Bikes. At the very heart of the application, the user will be presented with all bike stations in Dublin City. The user can pick any station and see relevant data such as bike and station availability. The user can plot a route from a fixed location. The user can also input an address and see the three closest stations in meters. The application also displays the current weather and temperature. The application will be able to show predictions (bikes available and parking spots available) based on a machine learning model trained on previous data provided for by JCDecaux (Bike and Stand Availability) and Open Weather (Weather API).

The application displays all Dublin bikes stations in Dublin City as bike pins. The user can click the individual pins or choose the name of the station from a dropdown box (If they do not know the location of the station on the map). The chosen station will appear as a smiley face emoji. This will then display the address, station number, whether it is open or not, bike and stand availability currently and predictions by the hour and week within the left-hand side of the screen. The application will also display current time, temperature, and weather.

![image](https://github.com/Fay3217/Dublin-Bike/blob/main/screenshot.png)

![image](https://github.com/Fay3217/Dublin-Bike/blob/main/screenshot2.png)

## Overall Structure ##

The technology stack used in our project is organized as shown in figure 11. We have utilized various existing libraries, including Google Maps for setting up the map, markers, and displaying routes, and Numpy, Sklearn, Pandas for machine learning. SQLAlchemy is used for accessing the database. For the backend, we use Python and Flask framework to implement most of the web functions. For the frontend, we use HTML, CSS, and primarily JavaScript language. In terms of data scraping and database building, we utilize some SQL commands, while Bash commands are used in EC2 establishment and application deployment processes, and Github is used for environment and code sharing as well as version control. In addition, we also use Trello and Google Docs for development progress design and control.

![image](https://github.com/Fay3217/Dublin-Bike/blob/main/structure2.png)
