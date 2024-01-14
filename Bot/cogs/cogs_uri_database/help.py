import discord
from discord.ext import commands
from functionality.utils import *
import os

try:
    PREFIX = os.environ["PREFIX"]
except:
    PREFIX = "*"

class Help(commands.Cog):
    def __init__(self, client):
        self.bot = client # This is to pass the main bot to this cog.
        self.guild_data = self.bot.guild_info
        self.guild_list_data = self.bot.guild_info_list

    @commands.command(name="help", aliases=["h"]) # This decorator works for tranforming a function into a command function that the bot will recognize.
    async def help(self, ctx, *args):
        """Give commands list"""
        # check if guild is present
        if not checkIfGuildPresent(ctx.guild.id):
            # embed send
            embed = discord.Embed(
                description="You are not registered, please run `" + PREFIX + "setup` first",
                title="",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
            return
        
        guild = self.guild_data[str(ctx.guild.id)]
        prefix = guild.prefix
        commands = {}
        if guild.tag:
            # check if the guild has tags enabled
            commands = {f"```{prefix}add <Title> <URL> <Tag 1> <Tag2>...<TagN>```": "Add URL to database with the tags (1,2...N). If no title is provided, the program will try to retrieve it from the url, however, if none is found you will have to write it manually on Notion.",
                        f"```{prefix}search <Tag 1> <Tag2>...<TagN>```": "List of records with Tag1, Tag2...Tag N",
                        f"```{prefix}searchTitle <Title>```": "List of records with the title",
                        f"```{prefix}delete <Tag1> <Tag2>....<TagN>```": "To delete record having tag 1,2...N. Will give list of records. Type in the serial number of the record you want to delete",
                        f"```{prefix}deleteTitle <Title>```": "To delete record having the title. Will give list of records. Type in the serial number of the record you want to delete",
                        f"```{prefix}upload <Tag 1> <Tag2>...<TagN>```": "Drag and drop the file and use this command in the comment section. It will upload it on the notion database with Tag 1,2.....N.",
                        f"```{prefix}prefix```": "Change the prefix of the bot",
                        f'```{prefix}setup_db_list```':'Command for setting up the other database used with the to-do-list'
                        }
        else:
            # no tags enabled
            commands = {f"```{prefix}add <Title> <URL>```": "Add URL to database",
                        f"```{prefix}search <Title>```": "List of records with Title",
                        f"```{prefix}delete <Title>```": "To delete record having title. Will give list of records. Type in the serial number of the record you want to delete",
                        f"```{prefix}upload```": "Drag and drop the file and use this command in the comment section. It will upload it on the notion database with Title",
                        f"```{prefix}prefix```": "Change the prefix of the bot",
                        f'```{prefix}setup_db_list```':'Command for setting up the other database used with the to-do-list'
                        }

        embed = discord.Embed(title="List of commands for the URI storage table:", description="These are the commands to use with this bot", color=discord.Color.blue())
        count = 1
        for command in commands:
                embed.add_field(name=str(count)+". "+ command, value=commands[command], inline=False)
                count += 1
        await ctx.send(embed=embed)

        # The show completed and uncompleted will have levels of specification, if none given, they will show all.
        # The below section will only be executed if the database of the list-to-do is executed.

        if(self.guild_list_data[str(ctx.guild.id)]):

            # The command to check uncompleted to completed status is missing.
            # Additonal column information updates are missing too.
            list_commands = {
                    f'```{prefix}addTask <Title> <Start Date> <End Date> <Type>```':'Add a new task. The format for dates is the following: Year-Month-Day (e.g. 2000-01-01, which represents January 1, 2000.',
                    f'```{prefix}changeTask <User>```':'Change the status of a task, from undone to done, or vice versa. Select the user and a menu with options will be shown, then choose the number of the task to be changed. Remember to enclose with double quote marks if you need to write a name with blank spaces (e.g. "Ruben Torres"), this applies for all the commands below.',
                    f'```{prefix}show_u <User>```':'Show uncompleted tasks. Add the user for only showing her/his tasks.',
                    f'```{prefix}show_c <User>```':'Show completed tasks. Add the user for only showing her/his tasks.',
                    f'```{prefix}deleteTask <User>```':'Delete a task by specifying the user, then a menu with her/his tasks will be shown, you select which you will erase.',
                    f'```{prefix}deleteAll_c <User1> <User2> ... <UserN>```':'This option will delete all completed tasks so far, one can specify if this will apply to only a set of users by giving the names.'
            }

            embed = discord.Embed(
                title="List of commands for the to-do list table:",
                description='These are the commands that will be performed to the other table with the tasks to do.',
                color=discord.Color.teal()
                )
            
            count = 1
            for command in list_commands:
                embed.add_field(name=str(count)+'. '+ command, value=list_commands[command],inline=False) # What is the purpose of value?
                count += 1

            embed.add_field(name='', value=chr(173), inline=False)
            embed.add_field(name='Additional comments:', value='    • The server nicknames of the users will take priority, if one was provided to you, then the original username will be considered as a different entity. Take this into consideration when adding and deleting records. \n\n    • All tags are lowercased.', inline=False)
            await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(Help(client))