import os
import discord
from dotenv import load_dotenv
import random
from discord.ext import commands
from googletrans import Translator
from requests import get

intents = discord.Intents.default()
intents.members = True

WELCOME_OPTIONS = ['愚蠢的西方人', '外国人', '鬼佬', '鬼子', '老外', '美国间谍',
'资本家', '资本主义猪', '安全威胁']

FORBIDDEN_WORDS = ['bad', 'stupid', 'worse', 'hate', 'overthrow', 'awful', 'dreadful', 'poor', 'cheap', 'imperfect', 'sucks', 'suck', 'trash', 'garbage', 'dislike', 'shit', 'fuck', 'worst', 'terrible', 'dumb']
PRAISE_WORDS = ['good', '#1', 'number 1', 'great', 'fucks', 'pog', 'poggers', 'best', 'amazing', 'love', 'china#1', 'superior', 'praise']

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has properly joined discord...')
    print(f'{bot.user} Has Joined The Server {bot.guilds[0]}')

@bot.event
async def on_member_join(member): # Need to get the welcome function working
    guild = member.guild
    print(f'{member.name} Joined')
    if guild.system_channel != None:
        welcome_message = f'The {random.choice(WELCOME_OPTIONS)} @{member.name} has joined the server!'
        await guild.system_channel.send(welcome_message)
    else:
        return


@bot.command(name='server-ip', help='Displays the current IP of the Minecraft Server. Use in case of IP change.')
async def server_ip(ctx):
    ip = get('https://api.ipify.org').text
    await ctx.send(f'The Current Server IP is: {ip}')

@bot.event    
async def on_message(message):     
    if message.author == bot.user:
        return
    message_list = list()
    message_list = message.content.split(' ')
    for i in range(len(message_list)):
        if message_list[i].isalpha():
            message_list[i] = message_list[i].lower()
        elif message_list[i].isalnum() != True:
            message_list[i] = message_list[i].strip('!')
            message_list[i] = message_list[i].strip('.')
            message_list[i] = message_list[i].strip(',')
            message_list[i] = message_list[i].strip('-')
            message_list[i] = message_list[i].lower()
        else:
            continue 
    print(f'Processed Message: {message_list}')
    bad_word_check = any(other_word in message_list for other_word in FORBIDDEN_WORDS)
    praise_word_check = any(other_word in message_list for other_word in PRAISE_WORDS)

    if ('china' in message_list) and bad_word_check:
        response = '🇨🇳 This message has been reported to The Ministry of State Security 🇨🇳'
        await message.channel.send(response)
    elif ('china' in message_list) and praise_word_check:
        response = '🇨🇳 The People Of China Thank You For Your Kind Words. + 100 Social Credit 🇨🇳'
        await message.channel.send(response)
    elif 'taiwan' in message_list:
        response = '🇨🇳 Did You Mean Chinese Taipei? 🇨🇳'
        await message.channel.send(response)
    elif message.content == 'china' or message.content == 'China':
        response = '🇨🇳 China #1 🇨🇳'
        await message.channel.send(response)
    print('Checks Finished')
    await bot.process_commands(message)

bot.run(TOKEN)