import json
import os
import random
import re
import tempfile
from urllib import parse as urparse
from urllib import request as urreq

import requests
import tweepy
from dotenv import load_dotenv
from urllib3.util import Retry

from humblimage.logger import *

load_dotenv()


class humblimage:
    """
      This class is the main entry point for the humblimage application.
      It is responsible to get image from api, and post in twitter
    """

    # ? A variable that is used to store the environment variables.
    __env: dict = os.environ

    # ? A variable that is used to store the twitter api object.
    __tAPI: tweepy.API = None

    # ? A variable that is hold the logging system
    __logger = None


    # ? A variable that is used to store the session object.
    __reqSession: requests.session = None

    # ? A variable holds categories list
    categories: list = []

    def __init__(self) -> None:

        # * Adjust the logger settings
        self.__logger = customizeLogger().get()

        self.__logger.log(INFO, "initializing humblimage")

        # * Set the request session with retry conditions
        self.__reqSession = self.getRequestSession()

        # * Connect to twitter
        self.__tAPI = self.connectTwitter()


        # ? Checking if there is spesific categories to get image from
        if "IMG_CATEGORIES" in self.__env:
            self.__logger.log(INFO, f"Found categories: {self.__env['IMG_CATEGORIES']}")
            self.categories = re.split(r"\s*,\s*", self.__env["IMG_CATEGORIES"])


        # url = "https://images.unsplash.com/photo-1650366055161-6707e84a2301?crop=entropy&cs=tinysrgb&fm=jpg&ixid=MnwxMTMwMDl8MHwxfHJhbmRvbXx8fHx8fHx8fDE2NTI5NjIyNzQ&ixlib=rb-1.2.1&q=80"
        # print(urparse.parse_qs(urparse.urlparse(url).query))

        # lala = urreq.urlopen(url)

        # # * Download image from url and save
        # r = request("GET", url)
        # with tempfile.NamedTemporaryFile(mode="wb", suffix=".jpg", delete=False) as f:
        #     f.write(lala.read())
        #     f.flush()
        #     print(f.name)
        # # * upload media to twitter
        # media = self.__tAPI.media_upload(filename="test.jpg",additional_owners="3043189101")
        
        # # * post media to twitter
        # self.__tAPI.update_status(
        #     status="New bot test 2",
        #     media_ids=[media.media_id_string],
        # )

    def startPosting(self) -> int:

        # * Get the random image from unsplash
        
        
        with tempfile.NamedTemporaryFile(mode="wb+",prefix="humblimage_", suffix=".jpg", delete=False) as f:
            imageResponse = self.prepareImg()
            f.write(imageResponse['response'].read())
            f.flush()
            # os.startfile(f.name) open file

            # * upload media to twitter
            media = self.__tAPI.media_upload(filename=f.name, additional_owners="3043189101")

            # * post media to twitter
            testt = self.__tAPI.update_status(
                status=f"'{imageResponse['splash']['description'] if not imageResponse['splash']['description'] == None else imageResponse['splash']['alt_description'] if not imageResponse['splash']['alt_description'] == None else '' }'",
                media_ids=[media.media_id_string],
            )

            print(testt)

            self.__logger.log(INFO, f"Saved image to {f.name}")

        return 1 
    
    def prepareImg(self) -> dict:
        """
        This method responsible for prepare the image from unsplash api
        :return: A urlopen object
        """

        i = 0
        while i < 10:
            i += 1
            splash = self.getRandomSplash()
            url = splash["urls"]["regular"]
            r = urreq.urlopen(url)
            if int(r.headers['content-length']) < 5000000:
                return {
                    "splash": splash,
                    "url": url,
                    "response": r,
                }

        raise Exception("Could not get image lover than 5mb from unsplash")
        
    def getRequestSession(self) -> requests.session:
        """
        It creates a session object that will retry 5 times on 521, 500, 502, 503, and 504 errors
        :return: A session object
        """

        retry = Retry(
            total=5,
            status_forcelist=[521, 500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"],
            raise_on_status=False,
        )

        adapter = requests.adapters.HTTPAdapter(max_retries=retry)

        ss = requests.session()


        ss.mount("http://", adapter)
        ss.mount("https://", adapter)

        return ss

    """------------- Unsplash ----------------"""
    def getRandomSplash(self) -> json:
        """
        This method responsible for get random image from unsplash api
        :Unsplash Doc: https://unsplash.com/documentation#search-photos
        """

        # * Check if all credentials are set in env
        if "UNSPLASH_ACCESS_KEY" not in self.__env:
            self.__logger.log(ERROR, f"Missing env variable UNSPLASH_ACCESS_KEY")
            raise Exception(f"Missing env variable UNSPLASH_ACCESS_KEY")

        query = None if self.categories == [] else {'query': random.choice(self.categories)}


        # * Get the random image from unsplash
        r = self.__reqSession.get("https://api.unsplash.com/photos/random",params= '' if query == None else query, headers={"Authorization": f"Client-ID {self.__env['UNSPLASH_ACCESS_KEY']}"})

        # * Check if the request was successfull
        if r.status_code != 200:
            self.__logger.log(ERROR, f"Failed to get random image from unsplash api. Status code: {r.status_code}")
            raise Exception(f"Failed to get random image from unsplash api. Status code: {r.status_code}")

        # * Check if the returned image is already posted
        json = r.json()
        if self.isImagePosted(type="imageid", value=json["id"]):
            self.__logger.log(WARNING, f"Image already posted. Skipping to next image")
            return self.getRandomSplash()

        # * Return the json response
        return json

    """------------- Twitter ----------------"""
    def connectTwitter(self) -> tweepy.API:
        """
        This method responsive for connection beetwen Twitter api endpoint using env veriables
        :Tweepy Doc: https://docs.tweepy.org/en/stable/authentication.html
        """

        # * Check if all credentials are set in env
        for e in ["TWITTER_CONSUMER_KEY", "TWITTER_CONSUMER_SECRET", "TWITTER_ACCESS_TOKEN", "TWITTER_ACCESS_TOKEN_SECRET"]:
            if e not in self.__env:
                self.__logger.log(ERROR, f"Missing env variable {e}")
                raise Exception(f"Missing env variable {e}")

        # * Set authentication credentials
        tAOUTH = tweepy.OAuthHandler(
            consumer_key=self.__env["TWITTER_CONSUMER_KEY"],
            consumer_secret=self.__env["TWITTER_CONSUMER_SECRET"],
            access_token=self.__env["TWITTER_ACCESS_TOKEN"],
            access_token_secret=self.__env["TWITTER_ACCESS_TOKEN_SECRET"]
        ) 

        # * Set the api object
        tAPI = tweepy.API(tAOUTH, timeout=20)

        # * return the api object
        return tAPI

    """------------- API ----------------"""
    def isImagePosted(self, type: str = "imageid", value: str|int = None) -> bool:
        """
        This method responsible for check if the image was posted to twitter
        :return: True if the image was posted, False otherwise
        """

        # * Check if all credentials are set in env
        for e in ["API_ENDPOINT", "API_VERSION"]:
            if e not in self.__env:
                self.__logger.log(ERROR, f"Missing env variable {e}")
                raise Exception(f"Missing env variable {e}")

        # * Get the last image posted to twitter
        r = self.__reqSession.get(f"http://{self.__env['API_ENDPOINT']}/{self.__env['API_VERSION']}/search", params={"type": type, "value": value})
        json = r.json()

        # * Check if the request was successfull
        if r.status_code != 200:
            #if status code not 200 return false
            return False
        else:
            if "image" in json:
            #if request returend image return true
                return True
            elif "isOk" in json and json["isOk"] == True:
            #if request returend isOk return true
                return True
            
            return False













            