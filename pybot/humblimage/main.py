from distutils.util import strtobool
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

from concurrent.futures import ThreadPoolExecutor, as_completed, wait, ALL_COMPLETED
import time
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
    __reqSession: requests.Session = None

    # ? A variable holds categories list
    categories: list = []

    userAgent = "humbldump/1.0"

    def __init__(self) -> None:

        # * Adjust the logger settings
        self.__logger = customizeLogger().get()

        self.__logger.log(INFO, "initializing humblimage")

        # * Set the request session with retry conditions
        self.__reqSession = self.getRequestSession()

        # * Connect to twitter
        self.__tAPI = self.connectTwitter()

        self.userAgent = f"{self.__env['APP_NAME']}/{self.__env['APP_VERSION']}"


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

    def postImage(self) -> int:

        # * Check if env file has multiple post image feature open

        count = 2 if "POST_MULTIPLE_IMAGES" in self.__env and strtobool(self.__env['POST_MULTIPLE_IMAGES']) == True else 1
        """
            If in env file there is POST_MULTIPLE_IMAGES set to true,
            Post max 2 file to twitter
            For not posting 2 file everytime, we chose random 1 or 2 with weight on 1 is 80%
        """

        
       # Creating a thread pool executer with max workers of count and thread name prefix of
       # humblimage
        executer = ThreadPoolExecutor(max_workers=count, thread_name_prefix="humblimage")
        
        # List of thread pool executer
        execList = []

        # List of executer returns
        file_results = {
            "medias": [],
            "splashs": []
        }

        # * Loop for count times
        for i in range(count):
            # * Create a thread pool executer
            execList.append(executer.submit(self.uploadTwitter))

        # * Wait for all thread pool executer to finish
        for r in as_completed(execList):
            file_results['medias'].append(r.result()['media'])
            file_results['splashs'].append(r.result()['image'])
        
        tweet = self.__tAPI.update_status(
            status="New bot test",
            media_ids=[val.media_id for val in file_results['medias']]
        )
        
        self.savePostedImage(tweet=tweet, images=file_results['splashs'])
        exit(1)
        print(test)

        return 0
    
    def prepareImg(self) -> dict:
        """
        This method responsible for prepare the image from unsplash api
        :return: A Spash, URL, Urlopen dicts list
        """

        i = 0
        #Retry 10 times
        while i < 10:
            i += 1
            splash = self.getRandomSplash()
            url = splash["urls"]["regular"]
            r = urreq.urlopen(url)

            # We must check if the file is more then 5MB
            # https://developer.twitter.com/en/docs/twitter-api/v1/media/upload-media/overview
            if int(r.headers['content-length']) < 5000000:
                return {
                    "splash": splash,
                    "url": url,
                    "response": r,
                }

        raise Exception("Could not get image lover than 5mb from unsplash")
    


    def getRequestSession(self) -> requests.Session:
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

        ss = requests.Session()

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

    def uploadTwitter(self, count: int = 1) -> list:
        """
        > It takes an image from the Unsplash API, saves it to a temporary file, uploads it to the
        Twitter API, and returns the image and media objects
        
        :param count: The number of images to return. Default: 1. Maximum: 30, defaults to 1
        :type count: int (optional)
        :return: A dictionary with the image and media objects
        :link:  https://developer.twitter.com/en/docs/twitter-api/v1/media/upload-media/api-reference/post-media-upload
        """

        #? Create a tempfile for image response
        tempFile = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg", prefix="humblimage_", mode="wb")
        
        try:
            #? Image response from unsplash api
            imageResponse = self.prepareImg()

            #? Write image response buffer to the tempfile
            tempFile.write(imageResponse["response"].read())
            tempFile.flush()

            self.__logger.log(INFO, f"image {imageResponse['splash']['id']} saved to {tempFile.name}")
            # os.startfile(tempFile.name)

            #? Upload saved image to the Twitter api
            media = self.__tAPI.media_upload(filename=tempFile.name)
            
            if hasattr(media, "media_id"):
                self.__logger.log(INFO, f"Image uploaded to Twitter, Media ID: {media.media_id}")
        except Exception as e:
            raise Exception(e)
        finally:
            # ? Finally remove the tempfile
            tempFile.close()
            os.remove(tempFile.name)

        return {
            "image": imageResponse["splash"],
            "media": media
        }

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
        r = self.__reqSession.get(f"{self.__env['API_PROTOCOL']}://{self.__env['API_ENDPOINT']}:{self.__env['API_PORT']}/{self.__env['API_VERSION']}/search", params={"type": type, "value": value})
        json = r.json()

        # * Check if the request was successfull
        return False if r.status_code != 200 else True if ("image" in json) or ("isOk" in json and json["isOk"] == True) else False

    def savePostedImage(self, tweet: object = None, images : list = []) -> bool:
        # * Check if all credentials are set in env
        for e in ["API_ENDPOINT", "API_VERSION"]:
            if e not in self.__env:
                self.__logger.log(ERROR, f"Missing env variable {e}")
                raise Exception(f"Missing env variable {e}")

        # * Check if the tweet is valid
        if tweet == None:
            self.__logger.log(ERROR, f"Missing tweet object")
            raise Exception(f"Missing tweet object")
        
        # * Check if the images is valid
        if images == []:
            self.__logger.log(ERROR, f"Missing images list")
            raise Exception(f"Missing images list")
        
        # * Save the images to the database
        dataBody = {
            "tweet_id": tweet.id,
            "postedat": int(tweet.created_at.timestamp()),
            "images": [
                {
                    "image_id": img["id"],
                    "image_description": img["description"],
                    "image_alt_description": img['alt_description'],
                    "owner_id": img["user"]["id"],
                    "owner_username": img["user"]["username"],
                    "owner_name": img["user"]["name"],
                    "owner_twitter_username": img["user"]["twitter_username"],
                } for img in images
            ]
        }
        

        # * Save the posted image to the database
        test = self.__reqSession.get(f"{self.__env['API_PROTOCOL']}://{self.__env['API_ENDPOINT']}:{self.__env['API_PORT']}/{self.__env['API_VERSION']}/savePostedImage", params={"imageData":json.dumps(dataBody)}, headers={'user-agent': self.userAgent})
        print(test.json())
        
        return False
    




    @staticmethod
    def colorText(r, g, b, text):
        """
        It takes in three integers (r, g, b) and a string (text) and returns a string with the text
        colored in the rgb color
        :author: https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
        :param r: Red
        :param g: The green value of the color
        :param b: bold
        :param text: The text you want to be colored
        :return: The colorTest method is being returned.
        """
        return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)

        













