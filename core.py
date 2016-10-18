import asyncio
import discord
import argparse
import logging
import os
from audio import play, volume



logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d:%(message)s")
log = logging.getLogger(__name__)



clearconsole = lambda: os.system('cls')
clearconsole()

if not discord.opus.is_loaded():
    # the 'opus' library here is opus.dll on windows
    # or libopus.so on linux in the current directory
    # you should replace this with the location the
    # opus library is located in and with the proper filename.
    discord.opus.load_opus("libopus-0.dll")





class Bot(discord.Client):

    def __init__(self):
        super().__init__()
        self.message = None
        self.player = None
        self.voice = None
        self.current = None
        self.previous = None
        self.file_name = None


    async def on_message(self, message): #On a message
        #Start checking which command it was. Would like to use a switch statement but python doesnt have one.
        self.message = message
        antifurry = ["furry", "yiff", "meow"]
        for item in antifurry:
            if item in message.content:
                await self.delete_message(message)
                return

        if message.content.startswith('join') and any(message.author.roles[x].name == 'botmaster' for x in range(1, 10)): #When telling the bot to join a channel

            channel_name = message.content[4:].strip() #Format the message
            check = lambda c: c.name == channel_name and c.type == discord.ChannelType.voice
            channel = discord.utils.find(check, message.server.channels)

            if self.voice is not None:
                await self.voice.disconnect()
            self.voice = await self.join_voice_channel(channel)
            # self.starter = message.author
        elif message.content.startswith('play') and any(message.author.roles[x].name == 'botmaster' for x in range(1, 10)):
            playItem = message.content[4:].strip()
            if self.player is not None:
                self.player.stop()

            if self.voice is not None:
                await play(playItem, self)

        elif message.content.startswith('vol') and any(message.author.roles[x].name == 'botmaster' for x in range(1, 10)):
            vol = message.content[3:].strip()

            if self.player is not None:
                await volume(float(vol), self)


        elif message.content.startswith('stop') and any(message.author.roles[x].name == 'botmaster' for x in range(1, 10)):

            if self.player is not None and self.player.is_playing():
                self.player.stop()
                log.info("Stopped '{}' from playing".format(self.current))
            else:
                log.info("User attempted to stop a song while a song is not playing")


    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')


bot = Bot()
bot.run("nobody has to know")
