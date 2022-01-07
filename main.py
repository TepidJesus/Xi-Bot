import os
import discord
from discord import user
from dotenv import load_dotenv
import random
from discord.ext import commands
from requests import get
import json
from credit_keeper import CreditKeeper

credit_score_keeper = CreditKeeper()

intents = discord.Intents.default()
intents.members = True

WELCOME_OPTIONS = ['愚蠢的西方人', '外国人', '鬼佬', '鬼子', '老外', '美国间谍',
'资本家', '资本主义猪', '安全威胁']

FORBIDDEN_WORDS = ['bad', 'stupid', 'worse', 'hate', 'overthrow', 'awful', 'dreadful', 'poor', 'cheap', 'imperfect', 'sucks', 'suck', 'trash', 'garbage', 'dislike', 'shit', 'fuck', 'worst', 'terrible', 'dumb', 'cool', 'amazingly']
PRAISE_WORDS = ['good', '#1', 'number 1', 'great', 'fucks', 'pog', 'poggers', 'best', 'amazing', 'love', 'china#1', 'superior', 'praise', 'very']
CHINA_WORDS = ['china', 'chinese']
NEGATIONS = ['isn\'t', 'not', 'never', 'isnt']

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has properly joined discord...')
    print(f'{bot.user} Has Joined The Server {bot.guilds[0]}')
    credit_score_keeper.refresh_creditscores(guild_members=bot.get_all_members())
    
@bot.event
async def on_member_join(member):
    guild = member.guild
    print(f'{member.name} Joined')
    credit_score_keeper.refresh_creditscores(guild_members=bot.get_all_members())
    if guild.system_channel != None:
        welcome_message = f'The {random.choice(WELCOME_OPTIONS)} {member.name} has joined the server!'
        await guild.system_channel.send(welcome_message)
    else:
        return

@bot.command(name='server-ip', help='Displays the current IP of the Minecraft Server. Use in case of IP change.')
async def server_ip(ctx):
    ip = get('https://api.ipify.org').text
    await ctx.send(f'The Current Server IP is: {ip}')

@bot.command(name='show-credit')
async def dump_json(ctx):
    scores = credit_score_keeper.display_credit_scores()
    await ctx.send(scores)

@bot.command(name='my-credit')
async def my_credit(ctx):
    scores = credit_score_keeper.get_credit_score(ctx.message.author.name)
    await ctx.send(scores)

@bot.event    
async def on_message(message):
    print(message.author.name)     
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
    bad_word_check = any(other_word in message_list for other_word in FORBIDDEN_WORDS)
    praise_word_check = any(other_word in message_list for other_word in PRAISE_WORDS)
    china_check = any(other_word in message_list for other_word in CHINA_WORDS)
    for i in range(len(message_list)):
        if message_list[i] in PRAISE_WORDS and message_list[i-1] in NEGATIONS:
            bad_word_check = True
        elif message_list[i] in FORBIDDEN_WORDS and message_list[i-1] in NEGATIONS:
            bad_word_check = False
    print(f'Processed Message: {message_list}')
    

    if china_check and bad_word_check:
        response = '🇨🇳 This message has been reported to The Ministry of State Security 🇨🇳\n🇨🇳 10 Credit Points Have Been Deducted From Your Balance 🇨🇳'
        credit_score_keeper.alter_creditscore(member=message.author.name, points=-10)
        await message.channel.send(response)
    elif china_check and praise_word_check and bad_word_check != True:
        response = '🇨🇳 The People Of China Thank You For Your Kind Words 🇨🇳\n🇨🇳 1 Credit Point Has Been Added To Your Balance 🇨🇳'
        credit_score_keeper.alter_creditscore(member=message.author.name, points=1)
        await message.channel.send(response)
    elif 'taiwan' in message_list:
        response = '🇨🇳 Did You Mean Chinese Taipei? 🇨🇳'
        await message.channel.send(response)
    elif china_check:
        response = '🇨🇳 China #1 🇨🇳'
        await message.channel.send(response)
    await bot.process_commands(message)

bot.run(TOKEN)