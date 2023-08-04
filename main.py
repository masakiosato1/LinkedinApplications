#Imports
from functions.scraping_functions import *
from functions.page_loading_functions import *
from functions.data_functions import *
from definitions.credentials import *
from definitions.urls import *
from definitions.xpaths import *
from personalize_results import *
from postgres.postgres_connector import postgres_connector

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import sys
from wakepy import keep
import pandas as pd
from datetime import date
import psycopg2




# Start Driver
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--incognito")
driver = webdriver.Chrome(options=options)
driver.execute_script("window.onblur = function() { window.onfocus() }")



#Load the login_url, wait until the title says "Log In"
load_page_by_title(driver, login_url, "Log In")



#Try Logging in 
login_attempt_counter = 0
while login(driver) == False and login_attempt_counter < 5:
    load_page_by_title(driver, login_url, "Log In")
    login_attempt_counter += 1
if login_attempt_counter >= 5:
    print("Error: cannot connect to page")
    sys.exit(f"Website Title: {driver.title}\nCurrent URL: {driver.current_url}")


with keep.running() as k:
    #Scrape each page
    data = [] 
    for search_url in search_url_list:
        print("Running new search url")
        load_page_by_element(driver, search_url, list_of_listings_xpath)
        i = 1
        while i < 9:
            data = data + go_through_page(driver)
            print(f"Done with page {i}")
            i += 1
            try:
                click_object(driver, f"{page_xpath}[{i}]")
            except:
                break



    #Upload to database
    output_table_dict['table_name'] += f" {date.today()}"
    postgres_connector = postgres_connector()
    postgres_connector.insert_data(output_db_dict, output_table_dict, data)
