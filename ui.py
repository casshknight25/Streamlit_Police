import folium
import streamlit as st
from folium.plugins import Draw
import geopandas as gpd
import pandas  as pd
from pandas import json_normalize
from streamlit_folium import st_folium
import json
import requests
from utils.api import handle_point_geometry, handle_polygon_geometry
from utils.vis import crime_category_pie_chart, crime_location_bar_chart, crime_outcome_bar_chart, process_and_display_data

st.set_page_config(page_title='Crime Statistics',  layout='wide', initial_sidebar_state='auto')
st.header(":blue[UK Street Crime Statistics Explorer] :cop:")

# Create map with initial zoom and draw feature 
m = folium.Map(location=[55.9533, -3.1882], zoom_start=6)
Draw(export=True).add_to(m)

# Use columns to create layout of map and graph visualisations next to it 
c1, c2 = st.columns(2)
with c1:
    output = st_folium(m, width=1000, height=1000)

with c2:
    if "last_active_drawing" in output:
        feature = output["last_active_drawing"]
    
        if feature and "geometry" in feature and feature["geometry"]:
            geometry_type = feature["geometry"].get("type")
            try:
                if geometry_type == "Point":
                    data = handle_point_geometry(feature)
                elif geometry_type == "Polygon":
                    data = handle_polygon_geometry(feature)
                else:
                    st.write("Unhandled geometry type")
                process_and_display_data(data)
            except requests.exceptions.RequestException as e:
                st.warning(f"Error: {e}")
            except TypeError as e:
                st.write(f"Error: {e}")
                st.write("Incomplete or invalid geometry data")
        else:
            st.subheader("Please draw a shape to get crime statistics.")
            st.info("Either drop a point on the map to get location crime data or draw a shape for crime stats of the polygon")
