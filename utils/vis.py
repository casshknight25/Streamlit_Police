import plotly.express as px
import pandas as pd
from pandas import json_normalize
import streamlit as st

def crime_category_pie_chart(df):
    """ Create Pie Chart to show proprotion of crimes broken down by type"""
    category_counts = df['category'].value_counts().reset_index()
    category_counts.columns = ['category', 'count']
    fig = px.pie(category_counts, values='count', names='category', title='Crime by Category')
    st.plotly_chart(fig, theme="streamlit")


def crime_location_bar_chart(df):
    """Create a bar chart of number of crimes by location"""
    location_counts = df['location.street.name'].value_counts().reset_index()
    location_counts.columns = ['Location', 'Number of Crimes']
    fig = px.bar(location_counts, x='Location', y='Number of Crimes', title='Number of Crimes by Location')
    # Customize axis titles and orientation
    fig.update_layout(xaxis_title="Location", yaxis_title="Number of Crimes", xaxis_tickangle=-45)
    st.plotly_chart(fig, theme ='streamlit')


def crime_outcome_bar_chart(df):
    """Create a bar chart of crime outcome statistics"""
    outcome_counts = df['outcome_status.category'].value_counts().reset_index()
    outcome_counts.columns = ['Outcome', 'Number of Crimes']
    fig = px.bar(outcome_counts, x='Outcome', y='Number of Crimes', title='Crime Outcome Statistics')
    # Customize axis titles and orientation
    fig.update_layout(xaxis_title="Outcome", yaxis_title="Number of Crimes")
    st.plotly_chart(fig)


def process_and_display_data(data):
    """Handle JSON response to df and visualise crime statistics returned"""
    df = pd.DataFrame(json_normalize(data))
    if st.checkbox('Show the Data'):
        st.dataframe(df)
    crime_category_pie_chart(df)
    crime_outcome_bar_chart(df)
    crime_location_bar_chart(df)