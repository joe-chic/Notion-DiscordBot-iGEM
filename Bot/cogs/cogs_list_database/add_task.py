import asyncio
import discord
import functionality.database_list.addTask as AT
from discord.ext import commands
from dateutil.parser import parse

def is_date(string, fuzzy=False):
    
    if string.isdigit():
        return False
    
    try:
        parse(string,fuzzy=fuzzy)
        return True
    except ValueError:
        return False

class Add_list(commands.Cog):
    # From where does the guild_info come from in this case?

    def __init__(self,client):
        self.bot = client
        self.guild_data = self.bot.guild_info_list
    
    @commands.command(name='addTask')
    async def add_t(self,ctx,*args):

        client = self.guild_data[str(ctx.guild.id)]

        if len(args) == 0:
            # embed send

            async with ctx.typing():
                embed = discord.Embed(
                    title="Please enter a valid query, no entry was given.",
                    color=discord.Color.red(),
                )
                await ctx.send(embed=embed)

            return

        # add_t <Title> <Start Date> <End Date> <Type>

        title, start, end, type = 'Title', '2000-01-01', '2000-01-01', 'misc'
        # The nickname is taken into consideration, that is the name that will appear in the database, instead of the username...
        # Okay, so first, when displaying usernames, the 

        name = ctx.author.nick if ctx.author.nick else ctx.author.name 

        for i in range(len(args)):
            if(is_date(args[i])):
                # Fix thing with the title.
                title = ' '.join(args[:i]).strip()
                start = ''.join(args[i])
                end = ''.join(args[i+1])

                if i+2 < len(args):
                    type = ' '.join(args[i+2:]).strip().lower()
                break

            elif(i == len(args)-1 and start == None):
                title = ''.join(args[:])

        async with ctx.typing():
            ans = AT.sendListData(client.notion_api_key,client.notion_db_id,title,name,start,end,type)        
            
            print(type)

            if ans.status_code == 200:

                print(ans.text)

                embed = discord.Embed(
                    title='New task was added:',
                    color=discord.Color.green()
                    )
                
                embed.add_field(name='Title',value='> ' + title,inline=True)
                embed.add_field(name='Contribuitor',value='> ' +name,inline=True)
                embed.add_field(name='Start Date',value='> ' +start,inline=True)
                embed.add_field(name='End Date',value='> ' +end,inline=True)
                embed.add_field(name='Status',value='> ' +'   :x:',inline=True)
                embed.add_field(name='Type',value='> ' +type,inline=True)

                await ctx.send(embed=embed)

            else:
                print(ans.status_code)
                print(ans.text)
                embed = discord.Embed(
                    title='Something went wrong.',
                    description='Check it out, there was a mistake.',
                    color=discord.Color.red()
                    )
                await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(Add_list(client))