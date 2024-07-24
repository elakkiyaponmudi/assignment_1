from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import time
import pandas as pd

URL = 'https://www.redbus.in/online-booking/tsrtc/?utm_source=rtchometile'

def initialize_driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver

def load_page(driver, url):
    driver.get(url)
    time.sleep(3)

def locate_element_by_xpath(driver, xpath):
    return driver.find_element(By.XPATH, xpath)

def extract_bus_details(driver, route_name, route_link):
    try:
        view_buses = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "button"))
        )
        driver.execute_script("arguments[0].click();", view_buses)
        time.sleep(2)

        # Scroll to the bottom of the page
        ActionChains(driver).send_keys(Keys.END).perform()
        time.sleep(2)
        bus_elements = driver.find_elements(By.CLASS_NAME, 'clearfix.bus-item')
        
        bus_details = []
        for bus in bus_elements:
            bus_name = bus.find_element(By.XPATH, ".//div[@class='travels lh-24 f-bold d-color']").text
            bus_type = bus.find_element(By.XPATH, ".//div[@class='bus-type f-12 m-top-16 l-color evBus']").text
            departure_time = bus.find_element(By.XPATH, ".//div[@class='dp-time f-19 d-color f-bold']").text
            duration = bus.find_element(By.XPATH, ".//div[@class='dur l-color lh-24']").text
            starting_time = bus.find_element(By.XPATH, ".//div[@class='bp-time f-19 d-color disp-Inline']").text
            star_rating = bus.find_element(By.XPATH, ".//div[@class='rating-sec lh-24']").text
            price = bus.find_element(By.XPATH, ".//div[@class='fare d-block']").text
            seat_availability = bus.find_element(By.XPATH, ".//div[@class='seat-left m-top-30']").text

            bus_detail = {
                "Route_Name": route_name,
                "Route_Link": route_link,
                "Bus_Name": bus_name,
                "Bus_Type": bus_type,
                "Departure_Time": departure_time,
                "Duration": duration,
                "Starting_Time": starting_time,
                "Star_Rating": star_rating,
                "Price": price,
                "Seat_Availability": seat_availability
            }
            bus_details.append(bus_detail)
        return bus_details

    except Exception as e:
        print(f'Failed to extract bus details: {e}')
        return []

        
def scrape_bus_routes(driver):
    route_names = []
    route_links = []
    
    pages = driver.find_element(By.CLASS_NAME, "DC_117_paginationTable")
    for i in range(1, 4):
        if i > 1:
            next_page = pages.find_element(By.XPATH, f'.//div[contains(@class,"DC_117_pageTabs") and text()="{i}"]')
            action = ActionChains(driver)
            action.move_to_element(next_page).perform()
            time.sleep(2)
            next_page.click()
        
        routes = driver.find_elements(By.CLASS_NAME, "route")
        for route in routes:
            route_names.append(route.text)
            route_links.append(route.get_attribute('href'))
    
    return route_links, route_names

def scrape_all_pages():
    all_bus_details = []
    driver = None
    try:
        driver = initialize_driver()
        load_page(driver, URL)
        
        route_links, route_names = scrape_bus_routes(driver)
        
        for link, name in zip(route_links, route_names):
            driver.get(link)
            time.sleep(2)
            bus_details = extract_bus_details(driver, name, link)
            if bus_details:
                all_bus_details.extend(bus_details)

    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        if driver:
            driver.quit()

    return all_bus_details

all_bus_details = scrape_all_pages()

df = pd.DataFrame(all_bus_details)
df.to_csv('tsrtc_bus_details.csv', index=False)

