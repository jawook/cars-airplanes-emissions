# Energy Minute Calculator for Fuel Efficiency of Planes & Automobiles

This project was written in Python to collect data about fuel efficiency for popular passenger jets and automobiles and allow users to compare the impact of a variety of different options.

**Project Structure:**
* Data is gathered using the [Jupyter notebook](https://github.com/jawook/cars-airplanes-emissions/raw/main/dataCollector.ipynb) to aggregate and clean data from the two main sources
* The [dashboard](https://energyminuteplanesvsautos.streamlitapp.com/) is created using Streamlit and hosted on their [free service](https://streamlit.io)
* The [python script](https://github.com/jawook/cars-airplanes-emissions/raw/main/cars-airplanes-emissions.py) further shapes the data and performs relevant calculations and reports results to the user

**Data Sources & Key Assumptions:**
* Fuel economy for automobiles is gathered from the [Government of Canada's 2022 Fuel Consumption Guide](https://www.nrcan.gc.ca/sites/nrcan/files/oee/files/csv/MY2022%20Fuel%20Consumption%20Ratings.csv)
* Fuel economy for passenger jets is gathered from [this wikipedia page](https://en.wikipedia.org/wiki/Fuel_economy_in_aircraft) which is source from a variety of primary sources
* Linear adjustments to fuel economy are made based on changes to the airplane passenger load or vehicle passenger count - this inherently makes the assumption that fuel consumption is identical regardless of passenger load
* Greenhouse gas emissions are calculated using estimates of 2.3kg of CO2 per L of gasoline (assumes all vehicles burn gasoline, true emissions for diesel engines would be slightly higher) and 2.5kg of CO2 per L of aviation kerosene - sourced from [ghgprotocol.com](https://ghgprotocol.org/)
* Time estimates assume an average travel speed of 90km/h for automobile trips (assuming continuous travel at that speed) and 850km/h for airplane (plus 3 hours to cover check-in, boarding, taxiing, and de-planing)

This data is sources using reasonable estimates and transparent assumptions, but if you have any suggestions for improvement, please feel free to reach out.
