# Data Analysis Assignment: Hawaii Climate Exploration

This project analyzes Hawaii's weather data, including precipitation and temperature observations, using Python for data analysis and Flask for API development. The assignment is divided into two main components: exploratory data analysis (`climate_starter.ipynb`) and API development (`app.py`).

---

## Project Components

### 1. Exploratory Analysis (`climate_starter.ipynb`)
The Jupyter Notebook performs a detailed analysis of Hawaii's climate data, focusing on:
- **Precipitation Trends**: Visualizing the last 12 months of precipitation data.
- **Station Analysis**: Identifying the most active weather stations and their temperature statistics.
- **Temperature Distributions**: Analyzing temperature observations from the most active station.

Key Outputs:
- Precipitation bar chart for the last 12 months.
- Histogram of temperature observations at the most active station.
- Summary statistics for precipitation and temperature data.

---

### 2. Flask API Development (`app.py`)
The Flask application provides an API to access Hawaii's weather data through various endpoints. Users can retrieve precipitation, station, and temperature data dynamically.

API Routes:
- **`/`**: Lists all available API routes.
- **`/api/v1.0/precipitation`**: Returns the last 12 months of precipitation data as JSON.
- **`/api/v1.0/stations`**: Returns a list of all weather stations.
- **`/api/v1.0/tobs`**: Returns temperature observations for the most active station for the last 12 months.
- **`/api/v1.0/<start>`**: Returns the minimum, average, and maximum temperatures from a start date.
- **`/api/v1.0/<start>/<end>`**: Returns the minimum, average, and maximum temperatures for a specified date range.

Example API Usage:
- Retrieve precipitation data:

