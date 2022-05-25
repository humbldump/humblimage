
# humblimage - pybot
Python bot side of humblimage project




## ENV Variables

To run this project, you will need to add the following environment variables to your .env file

```python
VERSION='0.1.2'
AUTHOR='humbldump'
EMAIL='humbldump@protonmail.com'

#When this variable is true, bot will publish 1 or 2 image
POST_MULTIPLE_IMAGES = 'False'

#------> Self API Env's <------#
API_PROTOCOL = "https"
#? HTTP Protocol (http or https)
API_ENDPOINT = "localhost"
#? Endpoint of API Server
API_PORT = "443"
#? Port of API Server (https: 443 | http: 80)
API_VERSION = "v1"
#? API Version
API_USE_CERTIFICATE = "False"
#? Use Client Certificate while Server Api Call (True | False) check out clouflare client side certificates

#*------> Self APP Env's <------*#
APP_NAME = "humblimage"
#? App Name for User-Agent
APP_VERSION = "0.1.2"
#? App Version


#------> Unsplash API Env's <------#
IMG_CATEGORIES = 'art,rome,culture,,african,analog,analog,india'
UNSPLASH_ACCESS_KEY = 'unsplash-acc-key'
UNSPLASH_SECRET_KEY = 'unsplash-secret-key'
UNSPLASH_URL = 'https://api.unsplash.com/'
IMG_QUALITY = 'raw'
#? Quality of image (raw | regular | small | thumb)

#------> Twitter API Env's <------#
TWITTER_CONSUMER_KEY = 'tw-app-consumer-key'
TWITTER_CONSUMER_SECRET = 'tw-app-consumer-secret'
TWITTER_ACCESS_TOKEN = 'tw-client-acc-token'
TWITTER_ACCESS_TOKEN_SECRET = 'tw-client-acc-token-secret'

```
## Installation

Required Python 3.10 and Poetry

```bash
    Poetry install
```
    
## Usage

[-]Single Tweet
```bash
    python run.py --single
```

[-]Tweet every X minutes (default 30 minutes)
```bash
    python run.py --i=30
```

