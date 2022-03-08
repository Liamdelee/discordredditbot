# bot.py
import os
import requests
from discord.ext import commands
from dotenv import load_dotenv
import html

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
USERNAME = os.getenv('REDDIT_USERNAME')
PASSWORD = os.getenv('REDDIT_PASSWORD')
USERSCRIPT = os.getenv('USERSCRIPT')
SECRETTOKEN = os.getenv('SECRETTOKEN')
PARAMS = {'limit': 1}

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='BOT', help='Responds with the first picture + title')
async def nine_nine(ctx, args1):

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

    res = requests.get("https://oauth.reddit.com/r/" + args1 + "/new",
                    headers=headers, params=PARAMS)

    for post in res.json()['data']['children']:
        for image in post['data']['preview']['images']:
            imageFull = image['source']['url']
            imageFullUrl = html.unescape(imageFull)
            output_text = (post['data']['title'] + "\n" + imageFullUrl)
            await ctx.send(output_text)

bot.run(TOKEN)