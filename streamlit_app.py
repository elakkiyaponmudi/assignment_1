import streamlit as st
from sqlalchemy import create_engine, text

# Create the engine to connect to your database
engine = create_engine('mysql+pymysql://root:#ponmudi22@localhost/redbus')

def fetch_filtered_data(route_name, bus_name=None, departure_time=None, duration=None, price=None, bus_type=None, star_rating=None, seat_availability=None):
    # Base query with route_name filter
    query = "SELECT * FROM bus_routes WHERE Route_Name = :route_name"
    params = {"route_name": route_name}

    # Append filters if provided
    if bus_name:
        query += " AND Bus_Name = :bus_name"
        params["bus_name"] = bus_name

    if departure_time:
        query += " AND Departure_Time = :departure_time"
        params["departure_time"] = departure_time

    if duration:
        query += " AND Duration = :duration"
        params["duration"] = duration

    if price is not None:
        query += " AND Price <= :price"
        params["price"] = price

    if bus_type:
        query += " AND Bus_Type = :bus_type"
        params["bus_type"] = bus_type

    if star_rating:
        query += " AND Star_Rating = :star_rating"
        params["star_rating"] = star_rating

    if seat_availability:
        query += " AND Seat_Availability = :seat_availability"
        params["seat_availability"] = seat_availability

    # Execute the query and fetch the results
    with engine.connect() as connection:
        result = connection.execute(text(query), params)
        data = result.fetchall()

    return data

def fetch_distinct_values(route_name, column_name):
    query = f"SELECT DISTINCT {column_name} FROM bus_routes WHERE Route_Name = :route_name"
    with engine.connect() as connection:
        result = connection.execute(text(query), {"route_name": route_name})
        values = [row[0] for row in result.fetchall()]

    return values

def main():
    st.title('🚌 Red Bus Data')

    # Fetch distinct route names
    query_route_names = "SELECT DISTINCT Route_Name FROM bus_routes"
    with engine.connect() as connection:
        route_names_result = connection.execute(text(query_route_names))
        route_names = [row[0] for row in route_names_result.fetchall()]

    # Sidebar for selecting route name
    selected_route = st.sidebar.selectbox('Select Route Name', [None] + route_names)
    
    if selected_route:
        # Fetch distinct values for filters
        bus_names = fetch_distinct_values(selected_route, "Bus_Name")
        departure_times = fetch_distinct_values(selected_route, "Departure_Time")
        durations = fetch_distinct_values(selected_route, "Duration")
        bus_types = fetch_distinct_values(selected_route, "Bus_Type")
        star_ratings = fetch_distinct_values(selected_route, "Star_Rating")
        seat_availabilities = fetch_distinct_values(selected_route, "Seat_Availability")

        # Sidebar filters
        selected_bus_name = st.sidebar.selectbox('Filter by Bus Name', [None] + bus_names)
        selected_departure_time = st.sidebar.selectbox('Filter by Departure Time', [None] + departure_times)
        selected_duration = st.sidebar.selectbox('Filter by Duration', [None] + durations)
        selected_price = st.sidebar.number_input('Filter by Price (<=)', min_value=0, step=1)
        selected_bus_type = st.sidebar.selectbox('Filter by Bus Type', [None] + bus_types)
        selected_star_rating = st.sidebar.selectbox('Filter by Star Rating', [None] + star_ratings)
        selected_seat_availability = st.sidebar.selectbox('Filter by Seat Availability', [None] + seat_availabilities)

        # Fetch filtered data based on user selections
        filtered_data = fetch_filtered_data(route_name=selected_route,
                                            bus_name=selected_bus_name, 
                                            departure_time=selected_departure_time,
                                            duration=selected_duration, 
                                            price=selected_price if selected_price > 0 else None,
                                            bus_type=selected_bus_type,
                                            star_rating=selected_star_rating,
                                            seat_availability=selected_seat_availability)
        st.write(f"### Filtered Data for Route: {selected_route}")
        st.write(filtered_data)

if __name__ == "__main__":
    main()
