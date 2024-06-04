import requests
from pandas import json_normalize

def get_crime_data(url):
    """Fetch Crime Data from given URL"""
    response = requests.post(url)
    response.raise_for_status()
    return response.json()

def handle_point_geometry(feature):
    """Format Point Data to Send to API"""
    lat = feature["geometry"]["coordinates"][1]
    lng = feature["geometry"]["coordinates"][0]
    url_coordinates = f"lat={lat}&lng={lng}"
    url = f"https://data.police.uk/api/crimes-street/all-crime?{url_coordinates}"
    return get_crime_data(url)

def handle_polygon_geometry(feature):
    """Format Polygon Data to Send to API"""
    last_active_drawing_coordinates = feature["geometry"]["coordinates"]
    flattened_coordinates = last_active_drawing_coordinates[0]
    url_coordinates = ":".join([f"{lat},{lng}" for lng, lat in flattened_coordinates])
    url = f"https://data.police.uk/api/crimes-street/all-crime?poly={url_coordinates}"
    return get_crime_data(url)