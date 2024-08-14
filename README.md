# 🚌 Red Bus Data Scrapping and Streamlit Application

This project involves scraping bus route data from the Redbus website using Selenium and presenting it in a Streamlit application with various filtering options. The data is stored in a MySQL database.

## Project Structure

- **scraper.py**: Contains the Selenium web scraping script.
- **streamlit_main.py**: Contains the Streamlit application script.
- **README.md**: Project documentation.

## Getting Started

### Prerequisites

- Python 3.8 or later
- MySQL database
- Chrome browser
- ChromeDriver

### Installation


1. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

2. Setup MySQL database:

    - Create a MySQL database named `redbus`.
    - Create a table `bus_routes` with appropriate columns to store the scraped data.

3. Update `scraper.py` and `streamlit_main.py` with your MySQL connection details.

### Running the Scraper

1. Run the scraper to fetch bus route data:
    ```sh
    python scraper.py
    ```

2. The scraper will save the bus route details in `bus_details.csv` and load the data into the MySQL database.

### Running the Streamlit Application

1. Run the Streamlit application:
    ```sh
    streamlit run streamlit_app.py
    ```

2. Open your browser and navigate to the provided URL to use the application.

## Streamlit Application Features

- **Select Route Name**: Choose a route to view the bus details.
- **Filter Options**:
    - Route Name
    - Min Duration
    - Max Duration
    - Min Price
    - Max Price
    - Bus Type
    - Star Rating
    - Seat Availability

## Files

- **scraper.py**: Contains the script to scrape bus route data from the RSRTC Redbus website using Selenium.
- **streamlit_main.py**: Contains the Streamlit application script to display and filter the bus route data.
- **bus_details.csv**: CSV file containing the scraped bus route data.



- Ensure you have ChromeDriver installed and its path is correctly set.
- Update MySQL connection details as required.
- The scraping script uses a delay (`time.sleep()`) to ensure elements load properly.



