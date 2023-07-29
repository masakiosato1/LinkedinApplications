from definitions import *

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import sys


def wait_element_load(driver, xpath):
    done = False
    counter = 0
    while done == False and counter < 5:
        try:
            driver.find_element(By.XPATH, xpath)
            done = True
        except:
            time.sleep(1)
            counter += 1
            
    if counter >= 5:
        return False
    else:
        return True   
    
def load_page_by_element(driver, url, xpath):
    driver.get(url)
    while wait_element_load(driver, xpath) == False:
        driver.get(url)
    return

def wait_page_load(driver, text):
    counter = 0
    while text not in driver.title and counter < 5:
        time.sleep(1)
        counter += 1
    if counter >= 5:
        return False
    else:
        return True
    
def load_page_by_title(driver, url, text):
    driver.get(url)
    while wait_page_load(driver, text) == False:
        driver.get(url)
    return

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
            submit_button = driver.find_element(By.XPATH, submit_button_xpath)
            ActionChains(driver).move_to_element(submit_button).click(submit_button).perform()
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

def get_listing_info(driver):
    #Wait until listing informations is loaded
    counter = 0   
    loaded = False
    
    listing_title = "N/A"
    company_size = "N/A"
    job_type = "N/A"
    job_description = "N/A"
    company_name = "N/A"
    
    #Repeat scrape attempts until I fail 5 times
    while loaded == False and counter < 5:
        
        error_check = [0, 0, 0, 0, 0]
        try:
            if listing_title == "N/A":
                listing_title = driver.find_element(By.CLASS_NAME, "jobs-unified-top-card__job-title").text
        except:
            listing_title = "N/A"
            error_check[0] = 1
            
        try: 
            if company_size == "N/A":
                company_size = driver.find_element(By.XPATH, company_size_xpath).text
        except:
            company_size = "N/A"
            error_check[1] = 1
        
        try:
            if job_type == "N/A":
                job_type = driver.find_element(By.XPATH, job_type_xpath).text
        except:
            job_type = "N/A"
            error_check[2] = 1






        #job description
        # company name
        try:
            if job_type == "N/A":
                job_type = driver.find_element(By.XPATH, job_type_xpath).text
        except:
            job_type = "N/A"
            error_check[3] = 1
        

        try:
            if job_type == "N/A":
                job_type = driver.find_element(By.XPATH, job_type_xpath).text
        except:
            job_type = "N/A"
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
    
    return [listing_title, company_size, job_type]

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
            time.sleep(1)
            apply_button = driver.find_element(By.XPATH, apply_button_xpath)
            time.sleep(1)
            ActionChains(driver).move_to_element(apply_button).click(apply_button).perform()
            time.sleep(1)
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

def go_through_page(driver):
    list_of_listings = driver.find_elements(By.XPATH, list_of_listings_xpath)
    data = []
    i = 1
    attempt_counter = 0
    #t1 = datetime.now()

    
    #Make sure next listing is ready
    if wait_element_load(driver, list_of_listings_xpath) == False:
        sys.exit(f"Website Title: {driver.title}\nCurrent URL: {driver.current_url}")
    
    while i <= len(list_of_listings):
        
        #find apply button and read it
        button_text = ''
        if wait_element_load(driver, f"{apply_button_xpath}"):
            time.sleep(1)
            button_text = driver.find_element(By.XPATH, apply_button_xpath).text
            time.sleep(1)
        else:
            continue
            time.sleep(1)
        
        
        if attempt_counter > 10 or 'Easy' in button_text:
            attempt_counter = 0
            i += 1
            if 'Easy' in button_text:
                print("Skipping because Easy Apply")
            else:
                print("Error: Skipping this listing")
            
            #t1 = datetime.now()


        #Make sure correct listing is selected
        try:
            #This fails when my screen isn't focused on the browser
            tmp = f"/html/body/div[contains(@class, 'application-outlet')]/div[3]/div[4]/div/div/main/div/div[1]/div/ul/li[{i}]/div/div[contains(@class, 'jobs-search-results-list__list-item--active')]"
            driver.find_element(By.XPATH, tmp)
        except:
            #click the correct one and start over
            listing_to_click = driver.find_element(By.XPATH, f"{list_of_listings_xpath}[{i}]")
            ActionChains(driver).move_to_element(listing_to_click).click(listing_to_click).perform()
            time.sleep(3)
            attempt_counter += 1
            continue


        #Get Listing and go to next loop
        listing_info = get_listing_info(driver)
        listing_info.append(get_application_url(driver))
        data.append(listing_info)
        attempt_counter = 0
        i += 1
        
        #Close extra windows
        while len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[1])
            driver.close()
        driver.switch_to.window(driver.window_handles[0])
        
        
        
        #print(datetime.now() - t1)
        #t1 = datetime.now()
        #Click next listing
        if i <= len(list_of_listings):
            listing_to_click = driver.find_element(By.XPATH, f"{list_of_listings_xpath}[{i}]")
            ActionChains(driver).move_to_element(listing_to_click).click(listing_to_click).perform()
        else:
            #this page is over
            continue
    return data
