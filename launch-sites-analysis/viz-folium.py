import folium
import pandas as pd

# Import folium MarkerCluster plugin
from folium.plugins import MarkerCluster
# Import folium MousePosition plugin
from folium.plugins import MousePosition
# Import folium DivIcon plugin
from folium.features import DivIcon

## Task 1: Mark all launch sites on a map

# Download and read the `spacex_launch_geo.csv`
#from js import fetch
#import io

# Constants
DATA_DIR = '/Users/fpj/Development/python/spacey/data/'
DATA_FILE = 'spacex_launch_geo.csv'
#URL = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_geo.csv'
#resp = await fetch(URL)
#spacex_csv_file = io.BytesIO((await resp.arrayBuffer()).to_py())
spacex_csv_file=DATA_DIR+DATA_FILE
spacex_df=pd.read_csv(spacex_csv_file)
#
# Select relevant sub-columns: `Launch Site`, `Lat(Latitude)`, `Long(Longitude)`, `class`
spacex_df = spacex_df[['Launch Site', 'Lat', 'Long', 'class']]
launch_sites_df = spacex_df.groupby(['Launch Site'], as_index=False).first()
launch_sites_df = launch_sites_df[['Launch Site', 'Lat', 'Long']]
#
#print('Launch Sites head :\n', launch_sites_df.head())
#print('Number of Launch Sites: ', len(launch_sites_df.index))

# Start location is NASA Johnson Space Center
nasa_coordinate = [29.559684888503615, -95.0830971930759]
site_map = folium.Map(location=nasa_coordinate, zoom_start=10)

# Create a blue circle at NASA Johnson Space Center's coordinate with a popup label showing its name
circle = folium.Circle(nasa_coordinate, radius=1000, color='#4169E1', fill=True).add_child(folium.Popup('NASA Johnson Space Center'))
# Create a blue circle at NASA Johnson Space Center's coordinate with a icon showing its name
marker = folium.map.Marker(
    nasa_coordinate,
    # Create an icon as a text label
    icon=DivIcon(
        icon_size=(20,20),
        icon_anchor=(0,0),
        html='<div style="font-size: 12; color:#4169E1;"><b>%s</b></div>' % 'NASA JSC',
        )
    )
site_map.add_child(circle)
site_map.add_child(marker)
# Save the current map
site_map.save('map-nasa.html')
#
# Initalize a new map
site_map = folium.Map(location=nasa_coordinate, zoom_start=5)
# Add markers to the map for each launch site
for index, row in launch_sites_df.iterrows():
    launch_site = row['Launch Site']
    lat = row['Lat']
    long = row['Long']
    coordinate = [lat, long]
    #print('Launch Site: ', launch_site, ' Lat: ', lat, ' Long: ', long)
    # Create a marker with the launch site name
    circle = folium.Circle(coordinate, radius=1000, color='#4169E1', fill=True).add_child(folium.Popup(launch_site))
    marker = folium.map.Marker(
        coordinate,
        # Create an icon as a text label
        icon=DivIcon(
            icon_size=(20, 20),
            icon_anchor=(0, 0),
            html='<div style="font-size: 12; color:#4169E1;"><b>%s</b></div>' % launch_site,
            )
        )
    site_map.add_child(circle)
    site_map.add_child(marker)

site_map.save('map-launch-sites.html')

# Task 2: Mark the success/failed launches for each site on the map
# Add Marker cluster to the map
marker_cluster = MarkerCluster()
# By launch site check the 'class' value and set marker color green for 1 and red for 0
for index, row in spacex_df.iterrows():
    if row['class'] == 1:
        marker = folium.Marker([row['Lat'], row['Long']], icon=folium.Icon(color='green'), popup='Success')
    else:
        marker = folium.Marker([row['Lat'], row['Long']], icon=folium.Icon(color='red'), popup='Failure')
    marker_cluster.add_child(marker)
#
site_map.add_child(marker_cluster)
site_map.save('map-launch-success-failures.html')

# TASK 3: Calculate the distances between a launch site to its proximities

# Add Mouse Position to get the coordinate (Lat, Long) for a mouse over on the map
formatter = "function(num) {return L.Util.formatNum(num, 5);};"
mouse_position = MousePosition(
    position='topright',
    separator=' Long: ',
    empty_string='NaN',
    lng_first=False,
    num_digits=20,
    prefix='Lat:',
    lat_formatter=formatter,
    lng_formatter=formatter,
)

site_map.add_child(mouse_position)
site_map.save('map-launch-distance.html')

from math import sin, cos, sqrt, atan2, radians

def calculate_distance(lat1, lon1, lat2, lon2):
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

# find coordinate of the closet coastline
launch_site_lat = 28.563197  # Launch Latitude
launch_site_lon = -80.576820 # Launch Longitude
# e.g.,: Lat: 28.56367  Lon: -80.57163
coastline_lat = 28.56393
coastline_lon = -80.56803
distance_coastline = calculate_distance(launch_site_lat, launch_site_lon, coastline_lat, coastline_lon)

# Create and add a folium.Marker on your selected closest coastline point on the map
coordinate = [coastline_lat, coastline_lon]
distance_marker = folium.Marker(
    coordinate,
    icon=DivIcon(
        icon_size=(20,20),
        icon_anchor=(0,0),
        html='<div style="font-size: 12; color:#4169E1;"><b>%s</b></div>' % "{:10.2f} KM".format(distance_coastline),
        )
    )
# Create a folium.PolyLine object to connect the launch site to the closest coastline point
coordinates = [[launch_site_lat, launch_site_lon], [coastline_lat, coastline_lon]]
lines=folium.PolyLine(locations=coordinates, weight=1)
site_map.add_child(lines)
site_map.add_child(distance_marker)
site_map.save('map-launch-coastline.html')

# Find the distance to the nearest railway
# e.g.,: Lat: 28.57205  Lon: -80.58527
railway_lat = 28.57111
railway_lon = -80.58545
# Calculate the distance
distance_railway = calculate_distance(launch_site_lat, launch_site_lon, railway_lat, railway_lon)
# Create and add a folium.Marker on your selected closest railway point on the map
coordinate = [railway_lat, railway_lon]
distance_marker = folium.Marker(
    coordinate,
    icon=DivIcon(
        icon_size=(20,20),
        icon_anchor=(0,0),
        html='<div style="font-size: 12; color:#4169E1;"><b>%s</b></div>' % "{:10.2f} KM".format(distance_railway),
        )
    )
# Create a folium.PolyLine object to connect the launch site to the closest railway point
coordinates = [[launch_site_lat, launch_site_lon], [railway_lat, railway_lon]]
lines=folium.PolyLine(locations=coordinates, weight=1)
site_map.add_child(lines)
site_map.add_child(distance_marker)

# Find the distance to the nearest highway
highway_lat = 28.56373
highway_lon = -80.57083
distance_highway = calculate_distance(launch_site_lat, launch_site_lon, highway_lat, highway_lon)
coordinate = [highway_lat, highway_lon]
distance_marker = folium.Marker(
    coordinate,
    icon=DivIcon(
        icon_size=(20, 20),
        icon_anchor=(0, 0),
        html='<div style="font-size: 12; color:#4169E1;"><b>%s</b></div>' % "{:10.2f} KM".format(distance_highway),
        )
    )
# Create a folium.PolyLine object to connect the launch site to the closest highway point
coordinates = [[launch_site_lat, launch_site_lon], [highway_lat, highway_lon]]
lines=folium.PolyLine(locations=coordinates, weight=1)
site_map.add_child(lines)
site_map.add_child(distance_marker)
#
# Find the distance to the nearest city
city_lat = 28.10473
city_lon = -80.64531
distance_city = calculate_distance(launch_site_lat, launch_site_lon, city_lat, city_lon)
coordinate = [city_lat, city_lon]
distance_marker = folium.Marker(
    coordinate,
    icon=DivIcon(
        icon_size=(20, 20),
        icon_anchor=(0, 0),
        html='<div style="font-size: 12; color:#4169E1;"><b>%s</b></div>' % "{:10.2f} KM".format(distance_city),
        )
    )
# Create a folium.PolyLine object to connect the launch site to the closest city point
coordinates = [[launch_site_lat, launch_site_lon], [city_lat, city_lon]]
lines=folium.PolyLine(locations=coordinates, weight=1)
site_map.add_child(lines)
site_map.add_child(distance_marker)
#
site_map.save('map-launch-distances.html')