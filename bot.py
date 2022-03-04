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
        intents = discord.Intents.default()
        intents.members = True
        super().__init__(command_prefix='!', intents=intents)
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
            print(f'[INFO] {self.user} Has Connected To Discord...')
            print(f'[INFO] {self.user} Has Joined The Server {self.guilds[0]}')
            self.credit_score_keeper.refresh_creditscores(guild_members=self.get_all_members())


    async def on_voice_state_update(self, member, before, after):
        if member.name in self.credit_score_keeper.member_mute_list and after.channel != None and before.channel == None:
            try:
                await member.edit(mute=True)
                print(f'[INFO] A Member Who Is On The Mute List Has Joined A Channel. Ensuring They Are Muted')
            except:
                pass
        elif member.name in self.credit_score_keeper.member_deafen_list and after.channel != None and before.channel == None:
            try:
                await member.edit(deafen=True)
                print(f'[INFO] A Member Who Is On The Deafen List Has Joined A Channel. Ensuring They Are Deafened')
            except:
                pass
        elif member.name not in self.credit_score_keeper.member_mute_list and after.channel != None and before.channel == None:
            try:
                await member.edit(mute=False)
                print(f'[INFO] A Member Who Is No Longer The Mute List Has Joined A Channel. Ensuring They Are No Longer Deafened')
            except:
                pass
        elif member.name not in self.credit_score_keeper.member_deafen_list and after.channel != None and before.channel == None:
            try:
                await member.edit(deafen=False)
                print(f'[INFO] A Member Who Is Not On The Deafen List Has Joined A Channel. Ensuring They Are Deafened')
            except:
                pass

    async def on_member_join(self, member):
        guild = member.guild
        print(f'[INFO] {member.name} Joined')
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
                raw_sentiment_score, china_check = self.message_processor.run_message_checks(message = message.content, message_list = messsage_list)
                if china_check == True:
                    bot_response, credit_change = self.message_processor.choose_response(message = message, message_list = messsage_list, china_check = china_check, raw_sentiment_score = raw_sentiment_score)
                    if credit_change != None:
                        self.credit_score_keeper.alter_creditscore(member=message.author.name, points=credit_change)
                        if bot_response == None:
                            return
                        else:
                            await message.channel.send(bot_response)

            author_credit = self.credit_score_keeper.member_credit_check(member_name = message.author.name)
            if author_credit <= 800 and author_credit > 791:
                await message.channel.send('🇨🇳 Attention Citizen, Your Credit Score Has Dropped Below 800. If This Continues You Will Be Punished Accordingly  🇨🇳')
            elif author_credit < 791 and author_credit > 600:
                try: # Removing The Lower Punishment From The Member
                    await message.author.edit(mute=False)
                    self.credit_score_keeper.member_mute_list.remove(message.author.name)
                except:
                    pass
            elif author_credit < 600 and author_credit > 400:
                try:
                    self.credit_score_keeper.member_mute_list.append(message.author.name)
                    await message.author.edit(mute=True)
                except:
                    self.credit_score_keeper.member_mute_list.append(message.author.name)
                try: # Removing The Lower Punishment From The Member
                    await message.author.edit(deafen=False)
                    self.credit_score_keeper.member_deafen_list.remove(message.author.name)
                except:
                    pass
            elif author_credit < 400 and author_credit > 200:
                try: # Applying The Punishment To The Member
                    self.credit_score_keeper.member_deafen_list.append(message.author.name)
                    await message.author.edit(deafen=True)
                except:
                    self.credit_score_keeper.member_deafen_list.append(message.author.name)
            elif author_credit < 200:
                await message.author.guild.ban(user=message.author, delete_message_days=0, reason='The Credit Score Of This Citizen Reached Critical Levels. They Have Been Moved To A Re-education Center')
                await message.channel.send(f'🇨🇳 {message.author.name} Has Been Moved To A Re-education Center 🇨🇳')
                self.credit_score_keeper.alter_creditscore(message, points=20)

                
bot = XiBot()
bot.run(TOKEN)