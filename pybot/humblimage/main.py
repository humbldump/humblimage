

from requests import request

from humblimage.logger import *
from logging import INFO,CRITICAL,DEBUG,ERROR,WARNING,NOTSET

class humblimage:
  """
    This class is the main entry point for the humblimage application.
    It is responsible to get image from api, and post in twitter
  """

  #? A variable that is used to store the twitter api object.
  __twitter_api = None;

  #? A variable that is hold the logging system
  __logger  = None;


  def __init__(self) -> None:
    


    #* Adjust the logger settings
    self.__logger = customizeLogger().get()

    self.__logger.log(INFO, "initializing humblimage")