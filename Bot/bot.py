import asyncio
import discord
from discord.ext import commands
from functionality import setupBot, utils
import os
from database import SessionLocal, engine
import models
import requests
import json

# JSON is text written in javascript object notation. This package helps to parse JSON strings into python dictionaries or lists.
# It also helps to convert python objects into JSON strings. The conversion cannot only stop at strings, you can also convert to acquire
# JSON objects, arrays, numbers and certain boolean values.  
# What is the importance of adding this?

import functionality.utils as utils
import functionality.security as security

from functionality.setupBot import verifyDetails 
from functionality.utils import encrypt, fixDatabase
from functionality.security import getKey

# BASICS:
    # "Having your bot concurrent is a requirement for the bot to be able to run in multiple servers."

    # discord.py 
    # this library revolves around the concept of events.
    # What does async keyword do? Python provides coroutines, as well as async/await keywords for writing asynchronous programs.
    # What is a coroutine? What is an asynchronous program? 
    # Asynchronous programming is process that consists in 
    # There are a few libraries that make writing asynchronous code easier, such as AsyncIO and Twisted.
    # Asynchronous programs are used for applications that require high degree of concurrency.
    # What is the difference between concurrency and computer parallelism?
    # In computer science, concurrency is defined as the ability of a computer system to be able to handle different tasks or operations
    # at the same time.
    # "Why does giving slices of the CPU make the program faster instead of using the single unit to solve all tasks?" Sometimes it is necessary due to 
    # the necessity of a possible user to interact with a certain function inmediately, if there were no concurrency, the user would need to wait.
    # Slicing the CPU can make a program more productive if it needs to wait for an input too form the user, it can continue doing tasks behind.


    # What is the general structure of a discord bot? 

    # What is WebSocketAPI? It is a communication protocol for consistent, bi-directional, full duplex TCP connection from a user's web browser to a server.
    # The Transmission Control Protocol (TCP) is a set of transport rules that is used on top of IPs to ensure reliable transmission of packets.
    # What is packet based messaging? A message that is transmitted into the network is broken down into pieces of information called packets, these are transmitted serially by the network
    # adapter. The computer is then able to reassemble the packets of information to get the original message. Packet switching refers to the ability of transferring small pieces of information across various networks.

    # __init__ The init keyword is used for initializing a special type of method, a constructor.

# database setup
db = SessionLocal() # INSTANCE OF SESSIONMAKER CLASS. Session object.

# What is the purpose of using this?
models.Base.metadata.create_all(bind=engine) #Is used for making the table, it creates from all the classes that extent from base and creates tables.

# prefix data
prefix = ""
prefix_data = {}
prefix_data_list = {}


# cogs
cogs = ["cogs.cogs_uri_database.delete", "cogs.cogs_uri_database.search", "cogs.cogs_uri_database.add", "cogs.cogs_uri_database.upload", "cogs.cogs_uri_database.help",'cogs.cogs_list_database.add_task','cogs.cogs_list_database.show_task','cogs.cogs_list_database.delete_task','cogs.cogs_list_database.change_task'] # Why is it necessary to implement this list?

# These are the python paths to the cogs.

# What is a listener in a discord bot? A listener is defined as a class that contains logic that will be run whenever an event occurs.

# What is the purpose of having prefix data and cogs? What are these things? 
    # The prefixes are the strings used for initiating a command for the bot. They are strings used for beginning bot commands.
    # Cogs are python classes that subclasses commands. These classes inherit from discord.ext.commands.Cog . It encapsulates commands, event listeners, and other
    # related functionalities that one wishes to group together.
    # 
    # discord.ext.commands.Cog is a base class that is used to inherit the members for cogs.
    # This base class contains certain decorators such as @commands.Cog.listener() and @commands.command()
    # It also contains a setup function called bot.add_cog() which adds an instance of the bot to the cog.
    # There are life cycle methods such as cog_load() and cog_unload() which can be used for setup and cleanup tasks. 

try:
    prefix = os.environ["PREFIX"] # What is this? os.environ is a dictionary containing all the environment variables of the operating system.
except:
    prefix = "*"

try:
    token = os.environ["TOKEN"]
except:
    print("No token found, exiting...")
    exit()

# get prefixes from the database
def fillPrefix():
    global prefix_data # What is prefix data? 

    prefix_data = {} # What is the purpose of having a prefix_data? empty dictionary, global changes.
    guilds = db.query(models.Clients).all() # This returns a list.
    for guild in guilds:
        prefix_data[str(guild.guild_id)] = guild.prefix

# cog loading reloading (this is a definition)
async def reload_cogs():
    for cog in cogs:
        await bot.reload_extension(cog) # What does this function do? updates cogs if any change was done?

async def load_cogs():
    for cog in cogs:
        await bot.load_extension(cog)
        # What does bot.load_extension() do? 

# get prefix of the guild that triggered bot
def get_prefix(client, message):
    global prefix_data
    try:
        prefix = prefix_data[str(message.guild.id)]
    except:
        prefix = "*"
    return prefix

fillPrefix() # What is the purpose of having this?  

intents = discord.Intents.all() # This is for granting the bot with a set of common permissions that will allow it to behave accordingly.
intents.message_content = True

# ,intents=intents

bot = commands.Bot(command_prefix=(get_prefix), help_command=None, intents=intents)

# commands.Bot provides functionality to handle commands better, particulary for the prefixes

# The use of arroba at the beginning of lines, are used for function and class decorators.

# What is an internal list command?


# bot.command() is used in the main document file, commands.command() decorator is used in cog files.

# setup command
@bot.command(name="setup") 
async def setup(ctx):
    # What is the point of adding a global prefix_data [dictionary] ?
    # Prefix data stores the prefix for each unique server.
      
    global prefix_data

    setup_data = await setupBot.setupConversation(ctx, bot) # This function will send an 
    if setup_data is not None:
        guild_id = setup_data.guild_id
        prefix = setup_data.prefix

        # update prefix_data
        prefix_data[str(guild_id)] = prefix

        # update guild_info
        bot.guild_info[str(guild_id)] = setup_data
        # The above line is for passing the setup_data to a new attribute established within the bot instance.

        embed = discord.Embed(
            description="Setup complete",
            color=discord.Color.green(),
        )
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="Setup failed", description="Setup failed", color=discord.Color.red()
        )
        await ctx.send(embed=embed)

# ctx stands for context.

# This command will set up the database for the to do list.
@bot.command(name='setup_db_list')
async def setup_db_list(ctx):

    global prefix_data_list 
    
    # Getting the notion API key.

    embed = discord.Embed(description='Enter the notion API key:')
    await ctx.send(embed=embed)

    try:
        msg = await bot.wait_for(
            'message',
            check=lambda message : ctx.author == message.author,
            timeout=60
        )
    except asyncio.TimeoutError:
        embed = discord.Embed(
            title='TimeOut',
            description='You took too long to respond. Operation cancelled.',
            color=discord.Color.red()
            )
        ctx.send(embed=embed)

    NOTION_API_ID = msg.content.strip()

    embed = discord.Embed(description='Enter the database ID:')
    await ctx.send(embed=embed)
    try:
        # bot.wait_for()
        msg = await bot.wait_for(
            "message",
            check=lambda message: message.author == ctx.author,
            timeout=60
        )
    except asyncio.TimeoutError:
        embed = discord.Embed(
            title='TimeOut',
            description="You took too long to answer. Operation cancelled.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return

    list_id = msg.content.strip() # The .strip() function is for removing the leading and trailing whitespaces from a string.

    # Verifying the information.

    existence = await verifyDetails(NOTION_API_ID,list_id,ctx)

    if existence:
        
        client_list = db.query(models.List).filter(models.List.guild_id == ctx.guild.id).first()

        # Maybe the none is added if the above line fails.

        if client_list:
            # Update the database for the resepctive client.
            # What is the point of encryption?

            client_list.notion_api_key = encrypt(NOTION_API_ID)
            client_list.notion_db_id = encrypt(list_id)
            db.commit()
            embed = discord.Embed(
                title='Update.',
                description='The client has been successfully updated.',
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)

            prefix_data_list[str(ctx.guild.id)] = prefix
            
            bot.guild_info_list[str(ctx.guild.id)] = (
                models.List(
                    GUILD_ID=ctx.guild.id,
                    NOTION_API_ID = encrypt(NOTION_API_ID),
                    NOTION_DB_ID = encrypt(list_id),
                    preFIX = prefix
                )
            )

            embed = discord.Embed(
                description="Setup complete",
                color=discord.Color.green(),
                )
            await ctx.send(embed=embed)

        else:
            # Add new data to the database.

            create_new_list_obj = models.List(
                    GUILD_ID=ctx.guild.id,
                    NOTION_API_ID = encrypt(NOTION_API_ID),
                    NOTION_DB_ID = encrypt(list_id),
                    preFIX = prefix
                )

            db.add(create_new_list_obj)
            db.commit()

            prefix_data_list[str(ctx.guild.id)] = prefix
            bot.guild_info_list[str(ctx.guild.id)] = create_new_list_obj

            embed = discord.Embed(
                description="Setup complete",
                color=discord.Color.green(),
                )
            await ctx.send(embed=embed)

    else:
        embed = discord.Embed(
            title="Some error has occured.",
            description='The IDs given were not correct somehow, look it up.',
            color=discord.Color.red()
            )
        ctx.send(embed=embed)
        return False

@bot.command(name="prefix")
async def changePrefix(ctx):
    """
    Change the prefix of the bot
    """
    # Why one has to change the prefix in the database?
    global prefix
    if not utils.checkIfGuildPresent(ctx.guild.id):
            embed = discord.Embed(
                description="You are not registered, please run `" + prefix + "setup` first",
                title="",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
            return
    prefix = db.query(models.Clients).filter_by(guild_id=ctx.guild.id).first().prefix
    embed = discord.Embed(
        title="Enter the new prefix for your bot",
        description="Current prefix is : " + prefix,
    )
    await ctx.send(embed=embed)
    try:
        msg = await bot.wait_for(
            "message", check=lambda message: message.author == ctx.author, timeout=60
        )
    except asyncio.TimeoutError:
        embed = discord.Embed(
            title="Timed out",
            description="You took too long to respond",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)
        return
    new_prefix = msg.content.strip()
    #.strip() is used to remove any trailing or leading whitespaces in a string

    db.query(models.Clients).filter_by(guild_id=ctx.guild.id).update(
        {"prefix": new_prefix}
    )
    # models.Client is the table with the information of the bot in servers.
    # filter_by is for filtering the row in a specific criteria.

    try:
        db.commit() #commit() is to save permamently any change done to the database during a session.
    except Exception as e:
        print(e)
        await ctx.send("Something went wrong, please try again!")
        return
    embed = discord.Embed(
        title="Successfully updated prefix",
        description="Prefix changed to " + new_prefix,
        color=discord.Color.green(),
    )
    await ctx.send(embed=embed)

    # Update prefix_data and reload cogs
    global prefix_data
    prefix_data[str(ctx.guild.id)] = new_prefix
    
    # update guild_info
    bot.guild_info[str(ctx.guild.id)].prefix = new_prefix

# storing guild info in an attribute of bot so that all cogs can access
bot.guild_info = utils.getGuildInfo()  # This returns a dictionary with the information of the stored guilds. Fuck, this is it.

# New function to get the information of the guild list info
def getGuildListInfo(): # What is the purpose of this function?
    other_guilds = db.query(models.List).all()
    data = {}

    for guild in other_guilds:
        # The purpose of the following line is: To decrypt the ID and the key.
        if getKey(guild.notion_db_id) and getKey(guild.notion_api_key): 
           
            # all good
            data[str(guild.guild_id)] = models.List(
                guild.guild_id,
                getKey(guild.notion_api_key),
                getKey(guild.notion_db_id),
                guild.prefix
            )
            print(data[str(guild.guild_id)].notion_api_key)
            print(data[str(guild.guild_id)].notion_db_id)
            
        else:
            # database rescue 
            print("Database not encrypt! Start encryption")
            print("Database fixed")
            fixListDatabase() # Will this actually work with the list database?
            # This basically encrypts data if wasn't encrypted before.
            # The whole function gets round again.
            return getGuildListInfo()
            
    print(data)
    return data # returns the decrypted data with the information of the guilds.


def fixListDatabase():
    # update database
    guilds = db.query(models.List).all()
    data = {}
    for guild in guilds:
        data[str(guild.guild_id)] = guild
        # encrypt api key and db key
        guild.notion_api_key = encrypt(guild.notion_api_key)
        guild.notion_db_id = encrypt(guild.notion_db_id)
        # update
        db.commit()
    return data

# Get info of the guilds for the list database.
bot.guild_info_list = getGuildListInfo()

# loading all the cogs
asyncio.run(load_cogs())

try:
    bot.run(token) # What does this function do? The function that initiates the operations of the discord bot is this method. It takes as an argument the token.
except Exception as e:
    print(e)
    print("No token...exiting!")

# What is guilding information?