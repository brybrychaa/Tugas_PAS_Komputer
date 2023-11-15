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


intents = discord.Intents.all()
intents.members = True
intents.presences = True

client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name='The Coconut Song'))
    print("The bot is now ready for use!")
    print("------------------------------")

@client.command()
async def hello(ctx):
    await ctx.send("Hi! I am Tadbot! Nice to meet you!")

@client.command()
async def goodbye(ctx):
    await ctx.send("Goodbye! May peace be with you.")

@client.event
async def on_member_join(member):
    channel = client.get_channel(1129579603221020744)
    await channel.send(f"Welcome to the server, {member.mention}! Please have some tea.")

@client.event
async def on_member_remove(member):
    channel = client.get_channel(1129579603221020744)
    await channel.send(f"Goodbye, {member.mention}! We'll miss you!")

@client.command(pass_context=True)
# Remove @client.command decorator
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        if ctx.voice_client:
            await ctx.send("I am already in a voice channel.")
        else:
            try:
                await channel.connect()
            except discord.ClientException as e:
                await ctx.send(f"Error: {e}")
    else:
        await ctx.send("You are not in a voice channel. You must be in a voice channel to run this command!")

# Remove @commands.command decorator
async def leave(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
        await ctx.send("I have left the voice channel.")
    else:
        await ctx.send("I am not in a voice channel.")

# Register the commands without the decorators



@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    try:
        await member.kick(reason=reason)
        await ctx.send(f'User {member} has been kicked')
    except discord.Forbidden as e:
        await ctx.send(f"Error: {e}")

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have the necessary permissions to kick people.")
    else:
        await ctx.send(f"An error occurred: {error}")

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    try:
        await member.ban(reason=reason)
        await ctx.send(f'User {member} has been banned')
    except discord.Forbidden as e:
        await ctx.send(f"Error: {e}")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have the necessary permissions to ban people.")
    else:
        await ctx.send(f"An error occurred: {error}")

@client.event
async def on_message(message):
    if message.content == "ugly":
        await message.delete()
        await message.channel.send("Please do not utter that phrase! The owner will be upset if they heard about this.")
    await client.process_commands(message)

# Cog Listeners
class MyCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        channel = reaction.message.channel
        await channel.send(f"{user.name} added: {reaction.emoji}")

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        channel = reaction.message.channel
        await channel.send(f"{user.name} removed: {reaction.emoji}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return

        if "happy" in message.content:
            emoji = '😆'
            await message.add_reaction(emoji)

def setup(client):
    client.add_cog(MyCog(client))

client.run(token)
