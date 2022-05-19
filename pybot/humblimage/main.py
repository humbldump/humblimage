import os

from dotenv import load_dotenv
from requests import request

from humblimage.logger import *

import tweepy, json


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

    def __init__(self) -> None:

        # * Adjust the logger settings
        self.__logger = customizeLogger().get()

        self.__logger.log(INFO, "initializing humblimage")

        # * Connect to twitter
        self.__tAPI = self.connectTwitter()

        test = self.getRandomSplash()
        print(test)


    """------------- Unsplash ----------------"""
    def getRandomSplash(self) -> json:
        """
        This method responsible for get random image from unsplash api
        :Unsplash Doc: https://unsplash.com/documentation#search-photos
        """

        # * Get the random image from unsplash
        r = request("GET", "https://api.unsplash.com/photos/random", headers={"Authorization": f"Client-ID {self.__env['UNSPLASH_ACCESS_KEY']}"})

        # * Check if the request was successfull
        if r.status_code != 200:
            self.__logger.log(ERROR, f"Failed to get random image from unsplash api. Status code: {r.status_code}")
            raise Exception(f"Failed to get random image from unsplash api. Status code: {r.status_code}")

        # * Return the json response
        return r.json()

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
