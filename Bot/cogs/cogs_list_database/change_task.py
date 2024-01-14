import json
import discord
import asyncio
from discord.ext import commands 
import requests
import functionality.database_list.deleteTask as DT
import functionality.database_list.changeTask as CT
from cogs.cogs_list_database.delete_task import wait_message, verifyUser, displayUsers

class changeTask(commands.Cog):
    def __init__(self,client):
        self.bot = client
        self.guild_data = self.bot.guild_info_list

    @commands.command(name='changeTask')
    async def changeTask(self,ctx,*args):
        client = self.guild_data[str(ctx.guild.id)]
        notion_members = DT.getNotionUsers(client.notion_api_key,client.notion_db_id,[str(member.nick) if member.nick else str(member) for member in ctx.guild.members])

        async with ctx.typing():

            if len(args) == 0:
                    # embed send
                    embed = discord.Embed(
                        title="Please enter a valid query, no entry was given.",
                        color=discord.Color.red(),
                    )
                    await ctx.send(embed=embed)
                    return

            user = args[0]
            
            if(not verifyUser(user,ctx,notion_members)):
                await ctx.send('You have provided a nonexistant user, try again.')
                await displayUsers(ctx,notion_members)
                return

            objs = DT.retrieveTasks(client.notion_api_key,client.notion_db_id,user)

            print(objs,end='\n')

            if len(objs) > 0:
                    count = 1
                    embed = discord.Embed(
                    title=f'Tasks of {user}:',
                    color=discord.Color.green()
                    )
                    for obj in objs:        
                        embed.add_field(name='',value=f'{count}. {obj.title}', inline=False)
                        count+=1
                    await ctx.send(embed=embed)    
            else:
                embed = discord.Embed(
                title=f'{user} has no recorded task',
                color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                return    
                    
        def check(reply_user):
                return reply_user.author == ctx.author and reply_user.channel == ctx.channel            
        
        msg = await wait_message(self.bot,ctx,check)
        error = True
        no = 0

        while error:
            try:
                no = int(msg.content)
                
                if(no > 0 and no <= len(objs)):
                    error = False
                else:
                    await ctx.send('The number doesn\'t correspond to any task. Try again.')
                    msg = await wait_message(self.bot,ctx,check)
            except:
                await ctx.send('You have no provided a number, try again.')
                msg = await wait_message(self.bot,ctx,check)

        async with ctx.typing():
            if(CT.changeOneTask(client.notion_api_key,client.notion_db_id,objs[no-1])):
                stat = ':ballot_box_with_check:' if not(objs[no-1].status) else ':x:'
                embed = discord.Embed(title='Task has changed:',color=discord.Color.green())
                embed.add_field(name='Title',value='> '+objs[no-1].title,inline=True)
                embed.add_field(name='Contribuitor',value='> '+user,inline=True)
                embed.add_field(name=' ',value=' ',inline=False)
                embed.add_field(name='Start date',value='> '+objs[no-1].start,inline=True)
                embed.add_field(name='End date',value='> '+objs[no-1].end,inline=True)
                embed.add_field(name=' ',value=' ',inline=False)
                embed.add_field(name='Status',value='> '+stat,inline=True)
                embed.add_field(name='Type',value='> '+objs[no-1].type,inline=True)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title='Something went wrong.',color=discord.Color.red())
                await ctx.send(embed=embed)
            
async def setup(client):
    await client.add_cog(changeTask(client))