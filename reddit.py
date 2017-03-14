import asyncio
import discord.discord as discord
import requests
import re
import logging
import json
import random

logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d:%(message)s")
log = logging.getLogger(__name__)

async def gime(message, text, bot):
    print("https://www.reddit.com/r/{text}/.json".format(text=text))
    r = requests.get("https://www.reddit.com/r/{text}/.json".format(text=text), params={"count": 20}, headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36"})
    obj = json.loads(r.text)
    post = obj["data"]["children"][int(random.random()*20)]["data"]
    check = lambda c: c.name == "general"
    channel = discord.utils.find(check, message.server.channels)
    if "title" in post:
        await bot.send_message(channel , post["title"] ,tts=True)
    if len(post["selftext"])>0:
        await bot.send_message(channel , post["selftext"] ,tts=True)
    if "url" in post:
        await bot.send_message(channel , post["preview"]["images"][0]["source"]["url"] ,tts=False)
