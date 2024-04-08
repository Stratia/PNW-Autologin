from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import FirefoxOptions, FirefoxProfile
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium import webdriver
from utills import logger
import sys
import os

class PNW_SEL():
    def __init__(self) -> None:
         #  loading variables from .env file
        load_dotenv() 
        self.firefox_profile_directory = os.getenv("Firefox_Profile_Directory") #  Gets environmental varialbe from .env file
        self.setup() #  Setups selenium driver, required for script to function
        self.login() #  Goes to PNW Website

    def setup(self):
        """
        Setup selenium driver path and profile folder needed to do
        anything in the browser and established a 'headless browser' (No visual browser)
        """
        G_FirefoxProfile = FirefoxOptions() #  Creates FirefoxOptions object, to interact with
        G_FirefoxProfile.add_argument("--headless") #  No visual browser   
        try:
            G_FirefoxProfile.profile = FirefoxProfile(self.firefox_profile_directory) #  Sets current cookie profile (Transfers logins
            print("Profile Setup Complete")
        except Exception: # Likely if profile directory doesn't exist
            logger.logs("File-Not-Found Error");print("Error Occured: Check if profile exists [!]")
            sys.exit() #  Exiting, as without profile script wouldn't have logins

        self.driver = webdriver.Firefox(options=G_FirefoxProfile) # Applying options | options=G_FirefoxProfile
        print("Web Driver Initaited")

    def login(self):
        """
        'Logs' into PNW by going onto nation page, only works
        when user is already signed. 
        """
        try:
            self.driver.get("https://politicsandwar.com/account/") #  Goes to URL
        except:
            logger.logs("Connection Error");print("Error Occured: Check your internet connection [!]")
            sys.exit(1)

        try:
            # Checks for 'You must be logged in to view that page.' text, to determine if user is logged in
            element_presence = EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'You must be logged in to view that page.')]"))
            WebDriverWait(self.driver, 30).until(element_presence) # Waits untill parameter returns True untill timeout

        except NoSuchElementException: # Logged in | Element doesn't exist
            print("Login success")

        except Exception: #  General error
            print("Login failed [!]")
            self.driver.quit()

        else: #  If No error
            print("Login failed [!] --> Make sure you're logged in")
            self.driver.quit()
            
PNW_SEL()