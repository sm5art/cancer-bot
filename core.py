import asyncio
import discord.discord as discord
import audioop
import argparse
import array
import logging
import struct
import os
from audio import play, volume
from reddit import gime
import random
import time
import wave
import io


logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d:%(message)s")
log = logging.getLogger(__name__)

class FakeAudioSource():

    def __init__(self):
        self.SAMPLE_RATE = 48000
        self.SAMPLE_WIDTH = 4
        self.FRAME_LENGTH = 20
        self.SAMPLES_PER_FRAME = int(self.SAMPLE_RATE/1000*self.FRAME_LENGTH)
        self.CHUNK= self.SAMPLES_PER_FRAME * self.SAMPLE_WIDTH
        self.stream = Stream()

class Stream():
    def __init__(self):
        self.buffer = b""

    def write(self, data):
        self.buffer += data

    def read(self):
        temp_bucket = self.buffer
        self.buffer = b""
        return temp_bucket

class Bot(discord.Client):

    def __init__(self, number):
        super().__init__()
        self.handler = {}
        self.voice = None
        self.data = []
        self.channel = None
        self.buffer = FakeAudioSource()
        self.player = None
        self.parsing = False

    def command(self, name):
        def decor(func):
            self.handler[name] = func
        return decor

    async def on_speak(self, data, ssrc, timestamp, sequence):
        pass

    async def on_message(self, message):
        if message.author == self.user:
            return
        for i in self.handler.keys():
            if message.content.startswith(i):
                await self.handler[i](self, message)



    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')




bot = Bot("1")

@bot.command('retard join')
async def dkfa(bot, message):
    channel_name = message.content[4:].strip() #Format the message
    bot.channel = message.channel
    check = lambda c: c.name == channel_name and c.type == discord.ChannelType.voice
    channel = discord.utils.find(check, message.server.channels)

    if bot.voice is not None:
        await bot.voice.disconnect()
    bot.voice = await bot.join_voice_channel(channel)
    await bot.enable_voice_events()

@bot.command('play')
async def dingus(bot, message):
    if bot.player not in (None, 1) and bot.player.is_playing():
        bot.player.stop()
    await play(bot, message)

@bot.command('vol')
async def dingus(bot, message):
    await volume(bot, message)

@bot.command('bro')
async def bro(bot, message):
    check = lambda c: c.name == "general"
    channel = discord.utils.find(check, message.server.channels)
    await bot.send_message(channel, "bro memes")

@bot.command('wtf')
async def bro(bot, message):
    check = lambda c: c.name == "general"
    channel = discord.utils.find(check, message.sehannels)
    await bot.send_message(channel, "wtf")

@bot.command('join')
async def dkfa(bot, message):
    channel_name = message.content[4:].strip() #Format the message
    bot.channel = message.channel
    check = lambda c: c.name == channel_name and c.type == discord.ChannelType.voice
    channel = discord.utils.find(check, message.server.channels)

    if bot.voice is not None:
        await bot.voice.disconnect()
    bot.voice = await bot.join_voice_channel(channel)


class Mock(object):
    def __init__(self, content):
        self.content = content


@bot.command('!play')
async def listen(bot, message):
    msg = Mock("play shrek ear rape")
    if bot.player not in (None, 1) and bot.player.is_playing():
        bot.player.stop()
    await play(bot, msg)

@bot.command('listen')
async def listen(bot, message):
    while True:
        result = await bot.voice.socket.recv(4096)
        print( result)

@bot.command('gime')
async def whatever(bot, message):
    subreddit = message.content[4:].strip()
    await gime(message, subreddit, bot)

@bot.command('rng')
async def listen(bot, message):
    number = int(message.content[3:].strip())
    check = lambda c: c.name == "general"
    channel = discord.utils.find(check, message.server.channels)
    await bot.send_message(channel, str(int(random.random()*number)+1))

@bot.command('stop')
async def da(bot, message):
    if bot.player is not None and bot.player.is_playing():
        bot.player.stop()

bot.run("")
