import os
import discord
from discord import message
from discord.abc import Messageable
from dotenv import load_dotenv
import random

WELCOME_OPTIONS = ['愚蠢的西方人', '外国人', '鬼佬', '鬼子', '老外', '美国间谍',
'资本家', '资本主义猪']

FORBIDDEN_WORDS = ['bad', 'stupid', 'worse', 'hate', 'overthrow', 'awful', 'dreadful', 'poor', 'cheap', 'imperfect', 'sucks', 'suck', 'trash', 'garbage', 'dislike', 'shit', 'fuck', 'worst']
PRAISE_WORDS = ['good', '#1', 'number 1', 'great', 'fucks']
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
    message_list = list()
    message_list = message.content.split(' ')
    bad_word_check = any(other_word in message_list for other_word in FORBIDDEN_WORDS)
    praise_word_check = any(other_word in message_list for other_word in PRAISE_WORDS)
    if message.author == client.user:
        return
    elif ('china' in message_list or 'China' in message_list) and bad_word_check:
        response = '🇨🇳 This message has been reported to The Ministry of State Security 🇨🇳'
        await message.channel.send(response)
    elif ('china' in message_list or 'China' in message_list) and praise_word_check:
        response = '🇨🇳 The People Of China Thank You For Your Kind Words. +100 Social Credit 🇨🇳'
        await message.channel.send(response)
    elif message.content == 'China' or message.content == 'china':
        response = '🇨🇳 China #1 🇨🇳'
        await message.channel.send(response)

client.run(TOKEN)