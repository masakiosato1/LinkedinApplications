from definitions.credentials import *
from definitions.urls import *
from definitions.xpaths import *

from functions.page_loading_functions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import sys

def click_object(driver, xpath, attempt_limit = 3):
    for i in range(attempt_limit):
        try:
            next_page_button = driver.find_element(By.XPATH, xpath)
            ActionChains(driver).move_to_element(next_page_button).click(next_page_button).perform()
            time.sleep(1)
            return
        except:
            print("Failed to click object")
            if i > 2 and attempt_limit > 3:
                driver.refresh()
                time.sleep(5)
    print(f"Failed to click object {attempt_limit} times")
    print(f"Tried to click {xpath}")

def login(driver):
    #Check to make sure we're at the login page
    if "Log In" not in driver.title:
        print("Not actually at the login page")
        return False
    
    #Fill text fields
    try:
        driver.find_element("id", "session_key").send_keys(username)
        driver.find_element("id", "session_password").send_keys(password)
    except:
        print("Can't find login fields")
        return False
    
    #Click submit button
    counter = 0
    while "Feed" not in driver.title and counter < 5:
        try:
            click_object(driver, submit_button_xpath, 3)
        except:
            print("Can't find submit button")
            while "checkpoint" in driver.current_url: 
                time.sleep(1)
            if "Feed" in driver.title:
                return True
            return False
    
    #Error Catch after 5 login attemps
    if counter >= 5:
        print("Failed 5 login attempts")
        sys.exit(f"Website Title: {driver.title}\nCurrent URL: {driver.current_url}")
            
    return True

def read_job_description(driver, preferred_keywords):
    # read job description and decide whether the job is relevant enough
        # keywords
        # years required
    # returns true or false

    job_description = (
        driver
        .find_element(By.XPATH, job_description_xpath)
        .text
    )

    #keyword check
    keyword_count = 0
    for keyword in preferred_keywords:
        if keyword in job_description:
            keyword_count += 1


    #year check
    job_description_split = job_description.split(".")
    years = ""
    for sentence in job_description_split:
        if "year" in sentence:
            years += sentence



    return keyword_count, years

def get_listing_info(driver):

    listing_scrape_method = [
        By.CLASS_NAME,
        By.XPATH,
        By.XPATH,
        By.XPATH
    ]
    listing_scrape_key = [
        "jobs-unified-top-card__job-title",
        job_type_xpath,
        company_name_xpath,
        company_size_xpath
    ]
    listing_info = ['','','','']
    for i in range(len(listing_info)):
        counter = 0
        while True:
            try:
                listing_info[i] = driver.find_element(listing_scrape_method[i], listing_scrape_key[i]).text
                break
            except:
                counter += 1
            if counter >= 5:
                print(f"Failed to scrape object {i}")
                break

    return listing_info


    '''

    #Wait until listing informations is loaded
    counter = 0   
    loaded = False
    
    listing_title = "N/A"
    company_name = "N/A"
    company_size = "N/A"
    job_type = "N/A"
    job_description = "N/A"
    job_id = "N/A"

    
    #Repeat scrape attempts until I fail 5 times
    







    while loaded == False and counter < 5:
        
        error_check = [0, 0, 0, 0, 0, 0]
        try:
            if listing_title == "N/A":
                listing_title = driver.find_element(By.CLASS_NAME, "jobs-unified-top-card__job-title").text
        except:
            listing_title = "N/A"
            error_check[0] = 1
            
        try:
            if company_name == "N/A":
                company_name = driver.find_element(By.XPATH, company_name_xpath).text
        except:
            company_name = "N/A"
            error_check[1] = 1

        try: 
            if company_size == "N/A":
                company_size = driver.find_element(By.XPATH, company_size_xpath).text
        except:
            company_size = "N/A"
            error_check[2] = 1
        
        try:
            if job_type == "N/A":
                job_type = driver.find_element(By.XPATH, job_type_xpath).text
        except:
            job_type = "N/A"
            error_check[3] = 1

        try:
            if job_description == "N/A":
                job_description = driver.find_element(By.XPATH, job_description_xpath).text
        except:
            job_description = "N/A"
            error_check[4] = 1
        

        if max(error_check) == 1:
            loaded = False
            counter += 1
            time.sleep(2)
        else:
            loaded = True
            counter = 0

    #Error Catch
    if counter >= 5:
        print("Error: cannot load listing after 5 attempts")
    else:
        print("Successfully scraped listing info")
    
    #return [listing_title, company_name, company_size, job_type, job_description]
    return [listing_title, company_name, company_size, job_type]
    '''

def get_application_url(driver):
    
    #initialize application link
    listing_application_link = ''
    
    #close all pages except for the first page
    while len(driver.window_handles) > 1:
        driver.switch_to.window(driver.window_handles[1])
        driver.close()
    
    #click apply button, try up to 5 times
    attempt_counter = 0
    while attempt_counter < 5 and len(driver.window_handles) == 1:
        attempt_counter += 1
        if wait_element_load(driver, f"{apply_button_xpath}"):
            click_object(driver, apply_button_xpath)
        else:
            print("Cannot find apply button")
    
    #5 attempts error, just return no application link
    if attempt_counter >= 5:
        print(f"Number of windows: {len(driver.window_handles)}")
        print("Error: Cannot load application after 5 attempts")
        return 'N/A'
    
    #scrape url
    if len(driver.window_handles) == 2:
        driver.switch_to.window(driver.window_handles[1])
        listing_application_link = driver.current_url
    elif len(driver.window_handles) >= 3:
        print("Error: Apply button opened multiple tabs")
        listing_application_link = 'N/A'
    
    
    #close all unrelated tabs
    while len(driver.window_handles) > 1:
        driver.switch_to.window(driver.window_handles[1])
        driver.close()
    
    #print("Got Application Link")
    return listing_application_link

def get_listing_id(driver):
    link = driver.current_url
    i = link.find('currentJobId=')+13
    new_link = link[i:]
    current_listing_id = int(new_link[0:new_link.find('&')])
    return current_listing_id

def go_through_page(driver, listing_ids, preferred_keywords, today, keyword_match_matters):
    time.sleep(3)
    list_of_listings = driver.find_elements(By.XPATH, list_of_listings_xpath)
    data = []
    listing_index = 1
    attempt_counter = 0
    if wait_element_load(driver, list_of_listings_xpath) == False:
        sys.exit(f"Website Title: {driver.title}\nCurrent URL: {driver.current_url}")
    
    while listing_index <= len(list_of_listings):
        #print(f"listing_index: {listing_index}")
        #print(f"attempt_counter: {attempt_counter}")
        #print(f"window_count: {len(driver.window_handles)}")
        attempt_counter += 1
        if listing_index>55:
            print("Reached desired limit for this page")
            break


        #Close extra windowss
        while len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[1])
            driver.close()
            time.sleep(1)
        driver.switch_to.window(driver.window_handles[0])
        

        #click on listing i
        if listing_index <= len(list_of_listings):
            try:
                click_object(driver, f"{list_of_listings_xpath}[{listing_index}]")
            except:
                print("Couldn't click next listing")
                break
            #attempt_counter = 0
            #listing_index += 1
        else:
            #this page is over
            break

        
        #get current listing_id
        current_listing_id = get_listing_id(driver)


        #find apply button and read it
        button_text = ''
        if wait_element_load(driver, f"{apply_button_xpath}"):
            try:
                button_text = driver.find_element(By.XPATH, apply_button_xpath).text
            except:
                continue
        else:
            print("wait_element_load for apply button returned false")
            continue
        

        keyword_count, years = read_job_description(driver, preferred_keywords)


        #Potential Listing Skip
        if attempt_counter > 5:
            print("Error: Skipping this listing, exceeded 5 attempts")
            attempt_counter = 0
            listing_index += 1
            continue
        elif 'Easy' in button_text:
            print("Skipping because Easy Apply")
            attempt_counter = 0
            listing_index += 1
            continue
        elif button_text == 'No longer accepting applications':
            print("Skipping because no longer accepting applications")
            attempt_counter = 0
            listing_index += 1
            continue
        elif current_listing_id in listing_ids:
            print("Skipping because already scraped this listing")
            attempt_counter = 0
            listing_index += 1
            continue
        elif keyword_count == 0 and keyword_match_matters:
            print("Skipping because no keyword matches")
            attempt_counter = 0
            listing_index += 1
            continue
        else:
            print("Not skipping this listing")


        #Get Listing and go to next loop
        listing_info = [today, current_listing_id]
        listing_info += get_listing_info(driver)
        listing_info += [get_application_url(driver), keyword_count, years]
        data.append(listing_info)
        listing_ids.append(current_listing_id)


        attempt_counter = 0
        listing_index += 1
        
    return data, listing_ids