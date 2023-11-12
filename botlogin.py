import discord
from discord.ext import commands
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions
from discord.ext import commands
import os
from dotenv import load_dotenv
import json

if os.path.exists(os.getcwd() + "/config.json"):
    with open("./config.json") as f:
        configData = json.load(f)
else:
    configTemplate = {"Token": "", "Prefix": "!"}

    with open(os.getcwd() + "/config.json", "w+") as f:
        json.dump(configTemplate, f)

token = configData["Token"]
prefix = configData["Prefix"]

client = discord.Client(intents=discord.Intents.default())
intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix = '!', intents=intents)

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Activity(type = discord.ActivityType.listening, name='The Coconut Song'))
    print("The bot is now ready for use!")
    print("------------------------------")

#Greetings
@client.command()
async def hello(ctx):
    await ctx.send("Hi! I am Tadbot! Nice to meet you!")

#Goodbye
@client.command()
async def goodbye(ctx):
    await ctx.send("Goodbye! May peace be with you.")

#When Member Joins
@client.event
async def on_member_join(member):
    channel = client.get_channel(1129579603221020744)
    await channel.send("Welcome to the server! Please have some tea.")

#When Member Leaves
@client.event
async def on_member_remove(member):
    channel  = client.get_channel(1129579603221020744)
    await channel.send("Goodbye! We'll miss you!")

#Voice Channel Commands
@client.command(pass_context = True)
async def join(ctx):
    if(ctx.author.voice):
        channel = ctx.message.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("You are not in a voice channel, you must be in a voice channel in order to run this command!")

@client.command(pass_context = True)
async def leave(ctx):
    if(ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("I have left the voice channel.")
    else:
        await ctx.send("I am not in a voice channel.")

#Kick and Ban
@client.command()
@has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'User {member} has been kicked')
    await client.process_commands(f'User {member} has been kicked')
@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
       await ctx.send("You don't have the necessary permissions to kick people.")

@client.command()
@has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'User {member} has been banned')

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
       await ctx.send("You don't have the necessary permissions to ban people.")

#Bot React to Specfic Words on Messages
@client.event
async def on_message(message):

    if message.content == "ugly":
        await message.delete()
        await message.channel.send("Please do not utter that phrase! The owner will be upset if they heard about this.")

#Embed Message
@client.event
async def on_member_join(user:discord.Member, *, message=None):
    message = "Welcome to my server!"
    embed = discord.Embed(title=message)
    await user.send(embed=embed)

@commands.Cog.listener()
async def on_reaction_add(self, reaction, user):
    channel = reaction.message.channel
    await channel.send("user.name" + " added: " + reaction.emoji)

@commands.Cog.listener()
async def on_reaction_add(self, reaction, user):
    channel = reaction.message.channel
    await channel.send("user.name" + " removed: " + reaction.emoji)

@commands.Cog
async def on_message(self, message):

    if message.author == self.client.user:
        return
    
    if("happy") in message.content:
        emoji = '😆'
        await message.add_reaction(emoji)

def setup(client):
    client.add_cog(client)
client.run(token)
