import os
import discord
from dotenv import load_dotenv
import random
from discord.ext import commands
from googletrans import Translator

intents = discord.Intents.default()
intents.members = True

def translate_text(text_input):
    translator = Translator()
    translation = translator.translate(text = text_input, src='auto')
    print(translation)
    return translation

WELCOME_OPTIONS = ['愚蠢的西方人', '外国人', '鬼佬', '鬼子', '老外', '美国间谍',
'资本家', '资本主义猪']

FORBIDDEN_WORDS = ['bad', 'stupid', 'worse', 'hate', 'overthrow', 'awful', 'dreadful', 'poor', 'cheap', 'imperfect', 'sucks', 'suck', 'trash', 'garbage', 'dislike', 'shit', 'fuck', 'worst', 'terrible', 'dumb']
PRAISE_WORDS = ['good', '#1', 'number 1', 'great', 'fucks', 'pog', 'poggers', 'best', 'amazing']


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
        welcome_message = f'The {random.choice(WELCOME_OPTIONS)} {member.name} has joined the server!'
        await guild.system_channel.send(welcome_message)
    else:
        return

@bot.command(name='translate') # Finish Translate command using googletrans lib
async def translate(ctx, arg):
    print(arg)
    arg = arg.encode('utf-8')
    translator = Translator(service_urls=None, user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64)', raise_exception=False)
    print('Translator Initialised')
    print(f'ARG: {arg}')
    translation = translator.translate(arg)
    print(f'translatoin: {translation}')
    translation = 'Hi'
    await ctx.send(arg)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    message_list = list()
    message_list = message.content.split(' ')
    for i in range(len(message_list)):
        if message_list[i].isalpha():
            message_list[i] = message_list[i].lower()
        else:
            continue

    print(message_list)
    bad_word_check = any(other_word in message_list for other_word in FORBIDDEN_WORDS)
    praise_word_check = any(other_word in message_list for other_word in PRAISE_WORDS)

    if ('china' in message_list) and bad_word_check:
        response = '🇨🇳 This message has been reported to The Ministry of State Security 🇨🇳'
        await message.channel.send(response)
    elif ('china' in message_list) and praise_word_check:
        response = '🇨🇳 The People Of China Thank You For Your Kind Words. +100 Social Credit 🇨🇳'
        await message.channel.send(response)
    elif message.content == 'china' or message.content == 'China':
        response = '🇨🇳 China #1 🇨🇳'
        await message.channel.send(response)
    await bot.process_commands(message)

bot.run(TOKEN)