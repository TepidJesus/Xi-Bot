from dotenv import load_dotenv
from discord.ext import commands
import discord
import os
import random
from requests import get
from credit_keeper import CreditKeeper
from message_analyzer import Message_processor


WELCOME_OPTIONS = ['愚蠢的西方人', '外国人', '鬼佬', '鬼子', '老外', '美国间谍',
'资本家', '资本主义猪', '安全威胁']

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

class XiBot(commands.Bot):

    def __init__(self):
        super().__init__(command_prefix='!')
        intents = discord.Intents.default()
        intents.members = True
        self.credit_score_keeper = CreditKeeper()
        self.message_processor = Message_processor()

        @self.command(name='my-credit')
        async def my_credit(ctx):
            scores = self.credit_score_keeper.get_credit_score(ctx.message.author.name)
            await ctx.send(scores)

        @self.command(name='server-ip', help='Displays the current IP of the Minecraft Server. Use in case of IP change.')
        async def server_ip(ctx):
            ip = get('https://api.ipify.org').text
            await ctx.send(f'The Current Server IP is: {ip}')

        @self.command(name='show-credit')
        async def show_credit(ctx):
            scores = self.credit_score_keeper.display_credit_scores()
            await ctx.send(scores)
    
    async def on_ready(self):
            print(f'{self.user} has properly joined discord...')
            print(f'{self.user} Has Joined The Server {self.guilds[0]}')
            self.credit_score_keeper.refresh_creditscores(guild_members=self.get_all_members())

    async def on_member_join(self, member):
        guild = member.guild
        print(f'{member.name} Joined')
        self.credit_score_keeper.refresh_creditscores(guild_members=self.get_all_members())
        if guild.system_channel != None:
            welcome_message = f'The {random.choice(WELCOME_OPTIONS)} {member.name} has joined the server!'
            await guild.system_channel.send(welcome_message)
        else:
            return

    async def on_message(self, message):
            await bot.process_commands(message)
            if message.author == self.user:
                return
            else:
                messsage_list = self.message_processor.listify_message(message)
                bad_word_check, praise_word_check, china_check = self.message_processor.run_message_checks(messsage_list)
                bot_response = self.message_processor.choose_response(message = message, message_list= messsage_list, china_check = china_check, bad_word_check = bad_word_check, praise_word_check = praise_word_check)
            if bot_response == None:
                return
            else:
                await message.channel.send(bot_response)
                
bot = XiBot()
bot.run(TOKEN)