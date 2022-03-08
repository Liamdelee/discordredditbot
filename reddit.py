# reddit.py
import os
import requests
from dotenv import load_dotenv

# import html
import html

load_dotenv()
USERNAME = os.getenv('REDDIT_USERNAME')
PASSWORD = os.getenv('REDDIT_PASSWORD')
USERSCRIPT = os.getenv('USERSCRIPT')
SECRETTOKEN = os.getenv('SECRETTOKEN')
PARAMS = {'limit': 1}

# note that CLIENT_ID refers to 'personal use script' and SECRET_TOKEN to 'token'
auth = requests.auth.HTTPBasicAuth(USERSCRIPT, SECRETTOKEN)

# here we pass our login method (password), username, and password
data = {'grant_type': 'password',
        'username': USERNAME,
        'password': PASSWORD}

# setup our header info, which gives reddit a brief description of our app
headers = {'User-Agent': 'MyBot/0.0.1'}

# send our request for an OAuth token
res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=data, headers=headers)

# convert response to JSON and pull access_token value
TOKEN = res.json()['access_token']

# add authorization to our headers dictionary
headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

# while the token is valid (~2 hours) we just add headers=headers to our requests
# requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)

res = requests.get("https://oauth.reddit.com/r/test/new",
                   headers=headers, params=PARAMS)

print(res.json())

for post in res.json()['data']['children']:
    print(post['data']['title'])  # let's see what we get
    for image in post['data']['preview']['images']:
        imageFull = image['source']['url']
        imageFullUrl = html.unescape(imageFull)
        res = requests.get(imageFullUrl)
        print(imageFullUrl)
        print(res)