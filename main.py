import os
import discord
from discord import message
from dotenv import load_dotenv
import random
WELCOME_OPTIONS = ['愚蠢的西方人', '外国人', '鬼佬', '鬼子', '老外', '美国间谍',
'资本家', '资本主义猪']



load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has properly joined discord...')
    print(f'{client.user} Has Joined The Server {client.guilds[0]}')

@client.event
async def on_member_join(member):
    channel = client.get_channel(927423272516206605)
    await channel.send(f'The {random.choice(WELCOME_OPTIONS)} {member.name} has joined the server!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    elif message.content == 'China' or message.content == 'china':
        response = '🇨🇳 China #1 🇨🇳'
        await message.channel.send(response)

client.run(TOKEN)