import discord
from discord.ext import commands
import asyncio
import functionality.database_list.showStatus as SS
import functionality.database_list.deleteTask as DT
from cogs.cogs_list_database.delete_task import verifyUser, displayUsers 

class Show_list(commands.Cog):
    def __init__(self,client):
        self.bot = client
        self.guild_data = self.bot.guild_info_list

    @commands.command(name='show_c')
    async def show_c(self,ctx,*args):

        client = self.guild_data[str(ctx.guild.id)]
        notion_members = DT.getNotionUsers(client.notion_api_key,client.notion_db_id,[str(member.nick) if member.nick else str(member) for member in ctx.guild.members])

        if(len(args) == 0):
            async with ctx.typing():
                data = SS.showStatus(client.notion_api_key, client.notion_db_id, '', True)
                
                if(len(data['results']) == 0 ):
                    embed = discord.Embed(title='No results retrieved, there were no completed tasks.',color=discord.Color.red())
                    await ctx.send(embed=embed) 
                else:
                    embed = discord.Embed(title='The Completed tasks  :ballot_box_with_check:  are:',description='',color=discord.Color.green())
                    await ctx.send(embed=embed) 

                    for row in data['results']:
                        title = row['properties']['Title']['rich_text'][0]['plain_text']
                        contribuitor_name = row['properties']['Contributors']['title'][0]['plain_text']
                        start_date = row['properties']['Start date']['date']['start']
                        end_date = row['properties']['End date']['date']['start']
                        type_options = [option['name'] for option in row['properties']['Type']['multi_select']]
                        
                        embed = discord.Embed(title='',description='',color=discord.Color.green())
                        embed.add_field(name='Title',value='> '+title,inline=True)
                        embed.add_field(name='Contributor name',value='> '+contribuitor_name,inline=True)
                        embed.add_field(name=' ',value=' ',inline=False)
                        embed.add_field(name='Start date',value='> '+start_date,inline=True)
                        embed.add_field(name='End date',value='> '+end_date,inline=True)
                        embed.add_field(name=' ',value=' ',inline=False)
                        embed.add_field(name='Type',value='> '+type_options[0],inline=True)
                        await ctx.send(embed=embed) 
        else:
            async with ctx.typing():
                user = args[0]

                if(verifyUser(user,ctx,notion_members)):
                    data = SS.showStatus(client.notion_api_key, client.notion_db_id, user, True)

                    if(len(data['results']) == 0 ):
                        embed = discord.Embed(title='No results retrieved, there were no completed tasks.',color=discord.Color.red())
                        await ctx.send(embed=embed) 
                    else:
                        embed = discord.Embed(title='The completed tasks  :ballot_box_with_check:  are:',description='',color=discord.Color.green())
                        await ctx.send(embed=embed) 
                    
                        for row in data['results']:
                            title = row['properties']['Title']['rich_text'][0]['plain_text']
                            contribuitor_name = row['properties']['Contributors']['title'][0]['plain_text']
                            start_date = row['properties']['Start date']['date']['start']
                            end_date = row['properties']['End date']['date']['start']
                            type_options = [option['name'] for option in row['properties']['Type']['multi_select']]
                            
                            embed = discord.Embed(title='',description='',color=discord.Color.green())
                            embed.add_field(name='Title',value='> '+title,inline=True)
                            embed.add_field(name='Contributor name',value='> '+contribuitor_name,inline=True)
                            embed.add_field(name=' ',value=' ',inline=False)
                            embed.add_field(name='Start date',value='> '+start_date,inline=True)
                            embed.add_field(name='End date',value='> '+end_date,inline=True)
                            embed.add_field(name=' ',value=' ',inline=False)
                            embed.add_field(name='Type',value='> '+type_options[0],inline=True)
                            await ctx.send(embed=embed)
                    
                else:
                    await ctx.send('You have provided a nonexistant user, try again.')
                    await displayUsers(ctx,notion_members)
                    return

    @commands.command(name='show_u')
    async def show_u(self,ctx,*args):
        client = self.guild_data[str(ctx.guild.id)]
        notion_members = DT.getNotionUsers(client.notion_api_key,client.notion_db_id,[str(member.nick) if member.nick else str(member) for member in ctx.guild.members])

        if len(args) == 0 :
            async with ctx.typing():
                data = SS.showStatus(client.notion_api_key, client.notion_db_id, '', False)

                if(len(data['results']) == 0 ):
                    embed = discord.Embed(title='No results retrieved, there were no uncompleted tasks.',color=discord.Color.red())
                    await ctx.send(embed=embed) 
                else:
                    embed = discord.Embed(title='The uncompleted tasks  :x:  are:',description='',color=discord.Color.green())
                    await ctx.send(embed=embed) 
                
                    for row in data['results']:
                        title = row['properties']['Title']['rich_text'][0]['plain_text']
                        contribuitor_name = row['properties']['Contributors']['title'][0]['plain_text']
                        start_date = row['properties']['Start date']['date']['start']
                        end_date = row['properties']['End date']['date']['start']
                        type_options = [option['name'] for option in row['properties']['Type']['multi_select']]
                        
                        embed = discord.Embed(title='',description='',color=discord.Color.green())
                        embed.add_field(name='Title',value='> '+title,inline=True)
                        embed.add_field(name='Contributor name',value='> '+contribuitor_name,inline=True)
                        embed.add_field(name=' ',value=' ',inline=False)
                        embed.add_field(name='Start date',value='> '+start_date,inline=True)
                        embed.add_field(name='End date',value='> '+end_date,inline=True)
                        embed.add_field(name=' ',value=' ',inline=False)
                        embed.add_field(name='Type',value='> '+type_options[0],inline=True)
                        await ctx.send(embed=embed)
        else:
            async with ctx.typing():
                user = args[0]
                if(verifyUser(user,ctx,notion_members)):
                    
                    data = SS.showStatus(client.notion_api_key, client.notion_db_id, user, False)

                    if(len(data['results']) == 0 ):
                        embed = discord.Embed(title='No results retrieved, there were no uncompleted tasks.',color=discord.Color.red())
                        await ctx.send(embed=embed) 
                    else:
                        embed = discord.Embed(title='The uncompleted tasks  :x:  are:',description='',color=discord.Color.green())
                        await ctx.send(embed=embed) 
                    
                        for row in data['results']:
                            title = row['properties']['Title']['rich_text'][0]['plain_text']
                            contribuitor_name = row['properties']['Contributors']['title'][0]['plain_text']
                            start_date = row['properties']['Start date']['date']['start']
                            end_date = row['properties']['End date']['date']['start']
                            type_options = [option['name'] for option in row['properties']['Type']['multi_select']]
                            
                            embed = discord.Embed(title='',description='',color=discord.Color.green())
                            embed.add_field(name='Title',value='> '+title,inline=True)
                            embed.add_field(name='Contributor name',value='> '+contribuitor_name,inline=True)
                            embed.add_field(name=' ',value=' ',inline=False)
                            embed.add_field(name='Start date',value='> '+start_date,inline=True)
                            embed.add_field(name='End date',value='> '+end_date,inline=True)
                            embed.add_field(name=' ',value=' ',inline=False)
                            embed.add_field(name='Type',value='> '+type_options[0],inline=True)
                            await ctx.send(embed=embed)

                else:
                    await ctx.send('You have provided a nonexistant user, try again.')
                    await displayUsers(ctx,notion_members)
                    return

async def setup(client):
    await client.add_cog(Show_list(client))