import discord
import logging
import json

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

from ase import getMTAServerPlayers
from config import CONFIG

TOKEN = CONFIG.get('token', None)
IP = CONFIG.get('ip', None)
PORT = CONFIG.get('port', None)
TIMEOUT = CONFIG.get('timeout', None)

client = discord.Client()

def getMTAServerPlayersResponse(players):
    response = f"Players online: {len(players)}\n"
    response += "```"
    for i in range(len(players)):
        player = players[i]
        name = player.get('name', None)
        ping = player.get('ping', None)
        if name and ping:
            response += f"#{i+1} {name}\n"
    response += "```"
    return response

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    global IP, PORT, TIMEOUT
    if message.author == client.user:
        return

    if message.content.startswith('$players'):
        players, error = getMTAServerPlayers(IP, PORT, TIMEOUT)
        if error:
            await message.channel.send("Failed to connect to the MTA server, maybe it's offline?")
        else:
            await message.channel.send(getMTAServerPlayersResponse(players))

client.run(TOKEN)
