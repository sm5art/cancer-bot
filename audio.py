import asyncio
import youtube_dl
import discord
import requests
import re
import logging
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d:%(message)s")
log = logging.getLogger(__name__)

async def play(text, bot):
    r = requests.get("https://www.youtube.com/results", params={"search_query": text})
    soup = BeautifulSoup(r.text)
    a = soup.find_all("a",href = re.compile("^\/watch"))
    url = "https://www.youtube.com%s" % a[0]["href"]
    bot.player = await bot.voice.create_ytdl_player(url)
    bot.player.start()
    if bot.current is not None:
        bot.previous = bot.current

    bot.current = bot.player.title

async def volume(value, bot):
    bot.player.volume = value
