import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Connection to MySQL database using SQLAlchemy
engine = create_engine('mysql+pymysql://root:#ponmudi22@localhost/redbus')

def fetch_data(route_name):
    query = f"SELECT * FROM bus_routes WHERE Route_Name = '{route_name}'"
    df = pd.read_sql(query, engine)
    return df

def filter_data(df, star_rating=None, bus_type=None, bus_name=None):
    if star_rating:
        df = df[df['Star_Rating'] == star_rating]
    if bus_type:
        df = df[df['Bus_Type'] == bus_type]
    if bus_name:
        df = df[df['Bus_Name'] == bus_name]
    return df

def main():
    st.title('🚌 Red Bus Data')

    # Fetching distinct route names
    query_route_names = "SELECT DISTINCT Route_Name FROM bus_routes"
    route_names = pd.read_sql(query_route_names, engine)['Route_Name'].tolist()

    # Sidebar for selecting route name
    selected_route = st.sidebar.selectbox('Select Route Name', route_names)
    if selected_route:
        data = fetch_data(selected_route)
        st.write(f"### Data for Route: {selected_route}")
        st.write(data)

        # Filter by Star Rating
        star_ratings = data["Star_Rating"].unique()
        selected_star_rating = st.sidebar.selectbox('Filter by Star Rating', [None] + list(star_ratings))

        # Filter by Bus Type
        bus_types = data["Bus_Type"].unique()
        selected_bus_type = st.sidebar.selectbox('Filter by Bus Type', [None] + list(bus_types))

        # Filter by Bus Name
        bus_names = data["Bus_Name"].unique()
        selected_bus_name = st.sidebar.selectbox('Filter by Bus Name', [None] + list(bus_names))
        

if __name__ == "__main__":
    main()
