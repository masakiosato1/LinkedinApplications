from functions.scraping_functions import *
from functions.page_loading_functions import *
from functions.data_functions import *

from definitions.credentials import *
from definitions.urls import *
from definitions.xpaths import *
from personalize_results import *

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import sys
from wakepy import keep
import pandas as pd
from datetime import datetime




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




#Load Search Page
load_page_by_element(driver, search_url, list_of_listings_xpath)




#Scrape
i = 1
data = [] 
while i < 8:
    data = data + go_through_page(driver)
    print(f"Done with page {i}")
    i += 1
    next_page_button = driver.find_element(By.XPATH, f"{page_xpath}[{i}]")
    ActionChains(driver).move_to_element(next_page_button).click(next_page_button).perform()


# Create the pandas DataFrame
df00 = pd.DataFrame(data, columns = ['listing_title', 'company_name', 'company_size', 'job_type', 'job_description', 'application_url'])


#data filtering
df01 = filter_company_size(df00)
df02 = filter_company_name(df01)
df03 = filter_application_url(df02)


# Exporting to CSV
from pathlib import Path  
filepath = Path('/Users/masakiosato/Desktop/jobs1.csv')  
filepath.parent.mkdir(parents=True, exist_ok=True)  
df03.to_csv(filepath)  




