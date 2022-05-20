import os

from dotenv import load_dotenv
from requests import request

from humblimage.logger import *

import tweepy, json

from urllib import request as urreq, parse as urparse
import tempfile
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


        url = "https://images.unsplash.com/photo-1650366055161-6707e84a2301?crop=entropy&cs=tinysrgb&fm=jpg&ixid=MnwxMTMwMDl8MHwxfHJhbmRvbXx8fHx8fHx8fDE2NTI5NjIyNzQ&ixlib=rb-1.2.1&q=80"
        print(urparse.parse_qs(urparse.urlparse(url).query))

        lala = urreq.urlopen(url)

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
