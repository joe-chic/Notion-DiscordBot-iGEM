import discord
from discord.ext import commands
import asyncio
import functionality.database_list.deleteTask as DT

def verifyUser(user,ctx, add_notion) -> bool:
    # check server default usernames.
    for member in ctx.guild.members:
        if(user == str(member)):
            return True
    
    # check server nicknames of users
    for member in ctx.guild.members:
        if(user == str(member.nick)):
            return True
    
    # check Notion additional participants.
    for member in add_notion:
        if(user == member):
            return True
        
    return False

async def displayUsers(ctx,add_notion):
    embed = discord.Embed(title='Users of this server:',color=discord.Color.red())
    count = 1

    # Display server users:
    for member in ctx.guild.members:
        # Use nickname if possible.
        if(member.nick):
            embed.add_field(name='',value=f'{count}. {member.nick} <Nickname>', inline=False)
            count+=1
        # If no nickname is found, then use the username.
        else:
            embed.add_field(name='',value=f'{count}. {member}', inline=False)
            count+=1

    # Display additional Notion users:
    if(len(add_notion) > 0):
        embed.add_field(name='', value=chr(173), inline=False)
        embed.add_field(name='Other users found on Notion:',value='', inline=False)
        for member in add_notion:
            embed.add_field(name='',value=f'{count}. {member}', inline=False)
            count+=1

    await ctx.send(embed=embed)

async def wait_message(bot,ctx,check):
    try:
        msg = await bot.wait_for("message", check=check, timeout=60)
        return msg
    except asyncio.TimeoutError:
        embed = discord.Embed(
            title="No response",
            description=f"Waited for 60s no response received",
            color=discord.Color.red(),
        )
        await ctx.send("You have not responded for 60s so quitting!")
        return

class Delete_list(commands.Cog):
    def __init__(self,client):
            self.bot = client
            self.guild_data = self.bot.guild_info_list

    @commands.command(name='deleteTask')
    async def delete_t(self,ctx,*args):

        client = self.guild_data[str(ctx.guild.id)]
        notion_members = DT.getNotionUsers(client.notion_api_key,client.notion_db_id,[str(member.nick) if member.nick else str(member) for member in ctx.guild.members])
        
        if(len(args) == 0):
            async with ctx.typing():
                embed = discord.Embed(title='You haven\'t provided a username, please try again.',color=discord.Color.red())
                await ctx.send(embed=embed)
                await displayUsers(ctx,notion_members)
                return

        user = args[0]

        if verifyUser(user,ctx,notion_members): 
            async with ctx.typing():
                pages = DT.retrieveTasks(client.notion_api_key,client.notion_db_id,user)
                
                if len(pages) > 0:
                    count = 1
                    embed = discord.Embed(
                    title=f'Tasks of {user}:',
                    color=discord.Color.green()
                    )
                    for page in pages:        
                        embed.add_field(name='',value=f'{count}. {page.title}', inline=False)
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
                    
                    if(no > 0 and no <= len(pages)):
                        error = False
                    else:
                        await ctx.send('The number doesn\'t correspond to any task. Try again.')
                        msg = await wait_message(self.bot,ctx,check)
                except:
                    await ctx.send('You have no provided a number, try again.')
                    msg = await wait_message(self.bot,ctx,check)

            async with ctx.typing():
                res = DT.deleteTask(client.notion_api_key,pages[no-1].id)
                
                if(res):
                    embed = discord.Embed(
                        title='Your task has been sucessfully deleted. Congrats!!!, you are truly blessed.',
                        color=discord.Color.green()
                        )
                    await ctx.send(embed=embed)

        else:
            async with ctx.typing():
                await ctx.send('You have provided a nonexistant user, try again.')
                await displayUsers(ctx,notion_members)
                return

    @commands.command(name='deleteAll_c')
    async def delete_ALL_COMPLETED(self,ctx,*args):

        client = self.guild_data[str(ctx.guild.id)]
        notion_members = DT.getNotionUsers(client.notion_api_key,client.notion_db_id,[str(member.nick) if member.nick else str(member) for member in ctx.guild.members])

        if(len(args) == 0):
            async with ctx.typing():
                embed = discord.Embed(title='You haven\'t provided a username, please try again.',color=discord.Color.red())
                await ctx.send(embed=embed)
                await displayUsers(ctx,notion_members)
                return

        USERS = [i for i in args]

        for user in USERS:
            if(not verifyUser(user,ctx,notion_members)):
                await ctx.send(f'{user} doesn\'t exist in the server. It won\'t be taken into consideration')
                USERS.remove(user)
        
        async with ctx.typing():
            ans = DT.deleteAllCompleted(client.notion_api_key,client.notion_db_id,USERS,ctx)

            if(ans):
                embed = discord.Embed(
                    title='Everything went great, all the completed tasks from every provided user have been removed.',
                    color=discord.Color.green()
                )
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title='Something went awful.',
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(Delete_list(client))