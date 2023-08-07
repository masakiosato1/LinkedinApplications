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
#Try logging in
login_attempt_counter = 0
while login(driver) == False and login_attempt_counter < 5:
    load_page_by_title(driver, login_url, "Log In")
    login_attempt_counter += 1
if login_attempt_counter >= 5:
    print("Error: cannot connect to page")
    sys.exit(f"Website Title: {driver.title}\nCurrent URL: {driver.current_url}")



#Get list of previously scraped jobs
query = "select listing_id from jobs"
postgres_connector = postgres_connector()
listing_ids = postgres_connector.get_data(output_db_dict, query)



#Stay awake while the long stuff happens
with keep.running() as k:
    #Scrape each page
    data = [] 
    for search_url in search_url_list:
        print("Running new search url")
        load_page_by_element(driver, search_url, list_of_listings_xpath)
        i = 1
        while i < 9:
            new_data, listing_ids = go_through_page(driver, listing_ids)
            data += new_data
            print(f"Count of saved listing_ids: {len(listing_ids)}")
            print(f"Done with page {i}")
            i += 1
            try:
                click_object(driver, f"{page_xpath}[{i}]")
            except:
                break


    #data check
    for i in range(len(data)):
        data[i].append(date.today())
        for j in range(len(data[i])):
            try:
                if len(j) >= 255:
                    data[i][j] = data[i][j][0:254]
            except:
                continue



    #Upload to database
    try:
        postgres_connector = postgres_connector()
    except:
        print("already defined postres")
    postgres_connector.insert_data(output_db_dict, output_table_dict, data)
