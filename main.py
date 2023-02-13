import discord
from discord.ext import commands
import os
from datetime import datetime
from discord.colour import Color
from replit import db
# from online import online

def delete_keys():
  for k in db.keys():
    del db[k]

def find_keys(id):
  i = False

  for k in db.keys():
    i = True
    return True

  if i is False:
    return False

db['key1'] = 'key1'

token = os.environ['token']
prefix = "~"
intents = discord.Intents.all()

bot = commands.Bot(
  command_prefix = prefix, 
  case_insensitive = True,
  intents = intents
         
)
 
@bot.event
async def on_ready():
  print(f"{bot.user.name} <- Online ")
  delete_keys()

@bot.event
async def on_message(ctx):
  if ctx.author == bot.user:
    return
  guild = bot.get_guild(1074367139928088597)

  category = discord.utils.get(guild.categories, id = 1074707885331861504)
  viewable_roles = discord.utils.get(guild.roles, name = "Mod")
#Bot gets dm
  if not ctx.guild:
    if find_keys(ctx.author.id) is True:
      channel = bot.get_channel(db[str(ctx.author.id)])
      pass
    else:
      try:
        print("New User {} ".format(ctx.author.name))
        overwrites = {
          guild.default_role: discord.PermissionOverwrite
          (read_messages = False), 
          viewable_roles: discord.PermissionOverwrite
          (read_messages = True)
        }
        new_channel = await guild.create_text_channel(f"\
        {ctx.author.name}-modmail", overwrites = overwrites, category = category)
  
  
        db[str(ctx.author.id)] = new_channel.id
        db[str(new_channel.id)] = ctx.author.id
        channel = bot.get_channel(db[str(ctx.author.id)])
  
        embed = discord.Embed(title = "New DM", color = Color.random(), timestamp = datetime.utcnow(), description = ctx.content)
  
        embed.set_footer(icon_url=ctx.author.avatar_url, text='\
        Sent by {} • {}'.format(ctx.author.name,
        ctx.author.mention))
  
        embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
  
        await channel.send(embed = embed)
        await ctx.add_reaction(emoji = '✅')
      except:
        await ctx.add_reaction(emoji = '❌')
  
bot.run(token)
  
