from definitions.urls import *
from selenium.webdriver.common.by import By
import time


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
