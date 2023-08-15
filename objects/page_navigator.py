import time

class page_navigator:
    def __init__(self, driver):
        self.driver = driver
        
    def click_object(self, xpath, attempt_limit = 3):
        for i in range(attempt_limit):
            try:
                next_page_button = self.driver.find_element(By.XPATH, xpath)
                ActionChains(self.driver).move_to_element(next_page_button).click(next_page_button).perform()
                time.sleep(1)
                return
            except:
                print("Failed to click object")
                if i > 2 and attempt_limit > 3:
                    self.driver.refresh()
                    time.sleep(5)
        print(f"Failed to click object {attempt_limit} times")
        print(f"Tried to click {xpath}")


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