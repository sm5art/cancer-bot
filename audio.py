import asyncio
import youtube_dl
import discord.discord as discord
import requests
import re
import logging
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d:%(message)s")
log = logging.getLogger(__name__)

async def play(bot, message):
    bot.player = 1
    text = message.content[4:].strip()
    r = requests.get("https://www.youtube.com/results", params={"search_query": text})
    soup = BeautifulSoup(r.text)
    a = soup.find_all("a",href = re.compile("^\/watch"))
    print(a)
    url = "https://www.youtube.com%s" % a[0]["href"]
    bot.player = await bot.voice.create_ytdl_player(url)
    bot.player.volume = 0.4
    bot.player.start()


async def volume(bot, message):
    value = float(message.content[3:].strip())
    bot.player.volume = value
