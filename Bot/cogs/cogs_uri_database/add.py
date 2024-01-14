import os
import discord
from discord.ext import commands
from functionality.utils import *
from functionality.addRecord import *
import asyncio

try:
    PREFIX = os.environ["PREFIX"]
except:
    PREFIX = "*"

class Add(commands.Cog):
    def __init__(self, client):
        self.bot = client
        self.guild_data = self.bot.guild_info

        # What is bot.guild_info?

        # What is a message embed? An embed is a special way to display information, it is a type of message presentation that could be used for several purposes.
        # They are really helpful when it comes to separating information and personalize its display.

    @commands.command(name="add", aliases=["a"]) # In here the command was established.
    async def add(self, ctx, *args):
        if not checkIfGuildPresent(ctx.guild.id):
            embed = discord.Embed(
                description="You are not registered, please run `"
                + PREFIX
                + "setup` first",
                title="",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
            return
        # check if the guild has tags enabled
        # get guild id
        guild_id = ctx.guild.id
        # get guild info
        client = self.guild_data[str(guild_id)]

        # check if args are empty

        # What do you mean that args are empty?

        if len(args) == 0:
            # embed send
            embed = discord.Embed(
                title="Please enter a valid query",
                description="You can search by title by typing `"
                + client.prefix
                + "add <url>`",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
            return

        
        title = None
        url = None
        tag_shift = 0

        if(validators.url(args[0])):
            # get url
            url = args[0]
        else:
            for i in range(1,len(args)):
                if(validators.url(args[i])):
                    url = args[i]
                    title = ' '.join(args[0:i])
                    tag_shift = i
                    break   
            
            # this fundamentally changes the process of how the tags are extracted...

        # It almost seems that args is a list with the response contents. The key to adding the title is to understand how args work.

        # check if url is valid
                
        name = ctx.author.nick if ctx.author.nick else ctx.author.name 

        async with ctx.channel.typing():
            if checkURL(url):
                # get title

                if(title == None):
                    title = getTitle(url)
                
                # getTitle(url) comes from the module functionality


                # check if title is valid 
                # <why do you need to check if title is valid?> If the <tag> title was not found, then the function soup.find() returns nothing.
                if title:
                    # valid title received
                    # check if record already exists
                    if doesItExist(url, client.notion_api_key, client.notion_db_id):
                        print("here")
                        # record already exists
                        # embed send
                        embed = discord.Embed(
                            title="Record already exists",
                            description="",
                            color=discord.Color.red(),
                        )
                        await ctx.send(embed=embed)
                        return
                    # check if user has tag and contributor role
                else:
                    # title not able to extract
                    if doesItExist(url, client.notion_api_key, client.notion_db_id): # Will this be different?
                        # record already exists
                        # embed send
                        embed = discord.Embed(
                            title="Record already exists",
                            description="",
                            color=discord.Color.red(),
                        )
                        await ctx.send(embed=embed)
                        return
                    # ask for title from user
                    # start conversation
                    await ctx.send("Please enter a valid title")

                    def check(m):
                        return m.author == ctx.author and m.channel == ctx.channel

                        # This checks that the response was done by the same person who requested the command, and it was done in the same channel.

                    try:
                        msg = await self.bot.wait_for(
                            "message", check=check, timeout=60
                        )
                    except asyncio.TimeoutError:
                        await ctx.send("Timed out")
                        return
                    # check if title is valid
                    if msg.content:
                        # valid title received
                        title = msg.content # WHAT DO YOU MEAN? This is valid because the specific Title was just asked after notifying there is an invalidity.
                    else:
                        # invalid title
                        await ctx.send("Invalid title")
                        return

                # add data <NEEDS TO BE MODIFIED>
                try:
                    if client.tag:
                        # addData
                        tags = getTags(args,tag_shift) #  HOW ARE TAGS IDENTIFIED?
                        author = name.split("#")[0]
                        addAllData(
                            url,
                            client.notion_api_key,
                            client.notion_db_id,
                            author,
                            tags,
                            title,
                        )

                    else:
                        # addData
                        author = name.split("#")[0]
                        addDataWithoutTag(
                            url,
                            client.notion_api_key,
                            client.notion_db_id,
                            title,
                            author,
                        )
                    # send success message
                    # embed
                    embed = discord.Embed(
                        title="Success",
                        description="Record added successfully",
                        color=discord.Color.green(),
                    )
                    await ctx.send(embed=embed)
                except Exception as e:
                    print(e)
                    # embed
                    embed = discord.Embed(
                        title="Error",
                        description="Error adding record. Check notion database id and api key provided",
                        color=discord.Color.red(),
                    )
                    await ctx.send(embed=embed)
            else:
                # embed
                embed = discord.Embed(
                    title="Invalid URL",
                    description="Please enter a valid URL",
                    color=discord.Color.red(),
                )
                await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(Add(client))
