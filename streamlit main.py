import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text

# Create the engine to connect to your database
engine = create_engine('mysql+pymysql://root:#ponmudi22@localhost/redbus')

def fetch_filtered_data(route_name, min_duration=None, max_duration=None, min_price=None, max_price=None, bus_type=None, min_star_rating=None, max_star_rating=None, min_seat_availability=None, max_seat_availability=None):
    """
    Fetch filtered bus data based on the provided filters.
    """
    query = "SELECT * FROM bus_routes WHERE Route_Name = :route_name"
    params = {"route_name": route_name}

    if min_duration is not None and max_duration is not None:
        query += " AND Duration BETWEEN :min_duration AND :max_duration"
        params["min_duration"] = min_duration
        params["max_duration"] = max_duration

    if min_price is not None and max_price is not None:
        query += " AND Price BETWEEN :min_price AND :max_price"
        params["min_price"] = min_price
        params["max_price"] = max_price

    if bus_type:
        query += " AND Bus_Type = :bus_type"
        params["bus_type"] = bus_type

    if min_star_rating is not None and max_star_rating is not None:
        query += " AND Star_Rating BETWEEN :min_star_rating AND :max_star_rating"
        params["min_star_rating"] = min_star_rating
        params["max_star_rating"] = max_star_rating

    if min_seat_availability is not None and max_seat_availability is not None:
        query += " AND Seat_Availability BETWEEN :min_seat_availability AND :max_seat_availability"
        params["min_seat_availability"] = min_seat_availability
        params["max_seat_availability"] = max_seat_availability

    with engine.connect() as connection:
        result = connection.execute(text(query), params)
        data = result.fetchall()

    columns = result.keys()
    df = pd.DataFrame(data, columns=columns)
    return df

def fetch_distinct_values(route_name, column_name):
    """
    Fetch distinct values for a specific column based on the route name.
    """
    query = f"SELECT DISTINCT {column_name} FROM bus_routes WHERE Route_Name = :route_name"
    with engine.connect() as connection:
        result = connection.execute(text(query), {"route_name": route_name})
        values = [row[0] for row in result.fetchall()]
    return values

def fetch_route_names():
    """
    Fetch distinct route names from the database.
    """
    query = "SELECT DISTINCT Route_Name FROM bus_routes"
    with engine.connect() as connection:
        result = connection.execute(text(query))
        route_names = [row[0] for row in result.fetchall()]
    return route_names

def display_sidebar_filters(route_name):
    """
    Display sidebar filters and return the selected filter values.
    """
    durations = fetch_distinct_values(route_name, "Duration")
    bus_types = fetch_distinct_values(route_name, "Bus_Type")
    
    selected_bus_type = st.sidebar.selectbox('Filter by Bus Type', [None] + bus_types)
    min_duration = st.sidebar.selectbox('Min Duration', [None] + sorted(durations))
    max_duration = st.sidebar.selectbox('Max Duration', [None] + sorted(durations))
    min_price = st.sidebar.number_input('Min Price', min_value=0, step=1)
    max_price = st.sidebar.number_input('Max Price', min_value=0, step=1)

    # Star Rating Sliders
    min_star_rating = st.sidebar.slider('Min Star Rating', min_value=1, max_value=5, step=1, value=1)
    max_star_rating = st.sidebar.slider('Max Star Rating', min_value=min_star_rating, max_value=5, step=1, value=5)

    # Seat Availability Sliders
    min_seat_availability = st.sidebar.slider('Min Seat Availability (%)', min_value=0, max_value=100, step=1, value=0)
    max_seat_availability = st.sidebar.slider('Max Seat Availability (%)', min_value=min_seat_availability, max_value=100, step=1, value=100)

    filters = {
        "bus_type": selected_bus_type,
        "min_duration": min_duration,
        "max_duration": max_duration,
        "min_price": min_price if min_price > 0 else None,
        "max_price": max_price if max_price > 0 else None,
        "min_star_rating": min_star_rating,
        "max_star_rating": max_star_rating,
        "min_seat_availability": min_seat_availability,
        "max_seat_availability": max_seat_availability
    }

    return filters

def main():
    st.title('🚌 Red Bus Data')

    route_names = fetch_route_names()
    selected_route = st.sidebar.selectbox('Select Route Name', [None] + route_names)
    
    if selected_route:
        filters = display_sidebar_filters(selected_route)
        filtered_data = fetch_filtered_data(route_name=selected_route, **filters)
        
        st.write(f"### Filtered Data for Route: {selected_route}")
        st.dataframe(filtered_data)

if __name__ == "__main__":
    main()


  
