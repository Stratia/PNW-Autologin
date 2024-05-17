from dotenv import load_dotenv
from bs4 import BeautifulSoup
from utills import logger
import requests
import sys
import os

class PNW_REQ():
    def __init__(self) -> None:
        #  loading variables from .env file
        load_dotenv() 

        #  Gets environmental variables from .env fil
        self.PNW_Password = os.getenv("PNW_Password")
        self.PNW_Email = os.getenv("PNW_Email")

        #  Attempts login
        self.Login() 

    def Login(self):
        """
        This function logins to the PNW account by sending a login requests containing 
        the users email & password. When done the function will verify the requests through the
        Login_check() func.
        """
        URL = "https://politicsandwar.com/login/"
        
        # Information to send over URL
        Payload = {"email": self.PNW_Email,
                   "password": self.PNW_Password,
                   "loginform": "Login"}
        
        with requests.Session() as self.LoginSession: #  Creates session, will close when done
            try:
                POST = self.LoginSession.post(URL, data=Payload) # Sends information through POST request
                Req = self.LoginSession.get("https://politicsandwar.com/account/") # To trigger string "May not login" etc etc
                print("Login Request Sent")

            # From specific to exception errors, prevents specific errors being masked by general ones
            # When error occures, logs event to logs.txt
            except requests.exceptions.HTTPError as Error: # HTTP Erorr
                print("HTTP error:", Error);logger.logs("HTTP Error: ", Error)

            except requests.exceptions.ConnectionError as Error: # DNS failure, refused connection, etc
                print("Connection-Error: Check internet connection [!] -->", Error);logger.logs("Connection Error: ", Error)
                sys.exit()

            except requests.exceptions.Timeout as Error: # Retries
                print("Timeout-Error Occured: Retrying [!] -->", Error);logger.logs("Timeout Error: ", Error)
                for i in range(0,3): #  This needs to be tested
                    print("Retry: ", i)
                    self.Login()
                sys.exit()

            except requests.exceptions.RequestException as Error: # General Error | What the hell happenend?
                print(Error, "General Error: Something else occured -->", Error);logger.logs("General Error: ", Error)
                sys.exit()
            
            else: #  If no error occurs
                print("Verifying Login")
                self.Login_check()
                
    def Login_check(self):
        """
        Looks for a element on the account page to determine if the user is logged in
        if this text exists --> 'You must be logged in to view that page.' appears, user is not logged in 
        If text doesn't appear, user is logged in
        """
        #  Todo: Use a more robust login check method, this one seems dubious, as string may not always appear
        new = self.LoginSession.get("https://politicsandwar.com/login/")
        soup = BeautifulSoup(new.text, "html.parser")
        parse = soup.findAll(string="You must be logged in to view that page.")

        if parse == "You must be logged in to view that page.":
            print("Login Failed [!]")
        else:  
            print("Login Success")
PNW_REQ()