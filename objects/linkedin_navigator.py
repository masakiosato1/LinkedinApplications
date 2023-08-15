from definitions.xpaths import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import sys



class linkedin_navigator:
    def __init__(self, driver):
        self.driver = driver

    def login(self, username, password):
        #Check to make sure we're at the login page
        if "Log In" not in self.driver.title:
            print("Not actually at the login page")
            return False
        
        #Fill text fields
        try:
            self.driver.find_element("id", "session_key").send_keys(username)
            self.driver.find_element("id", "session_password").send_keys(password)
        except:
            print("Can't find login fields")
            return False
        
        #Click submit button
        counter = 0
        while "Feed" not in self.driver.title and counter < 5:
            try:
                self.click_object(submit_button_xpath)
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