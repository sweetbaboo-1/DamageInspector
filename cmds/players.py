import discord
import settings
from discord.ext import commands
from playerIDs import addPlayer, removePlayer, getPlayerIDs
from checks import is_owner

logger = settings.logging.getLogger("bot")

@commands.group()
async def players(ctx):
  if ctx.invoked_subcommand is None:
    await ctx.send("try !help player")

# This command should add a hero to the json file
@players.command(name='add')
@commands.check(is_owner)
async def add(ctx, member: discord.Member, id : int):
  """{@player, id}"""
  
  name = member.name
  logger.info("Trying to add player")
  await ctx.send(f"Adding hero {name} with id {id} to file")
  if addPlayer(name, id):
    logger.info(f"Added {name} with id {id}")
    await ctx.send(f"Successfully added {name}")
  else:
    logger.info(f"Failed to add {name} with id {id}")
    await ctx.send(f"Failed to add {name}")

# This command should remove a hero from the json file
@players.command(name='remove')
@commands.check(is_owner)
async def remove(ctx, member: discord.Member):
  """{name}"""
  
  name = member.name
  if removePlayer(name):
    logger.info(f"Removed {name}")
    await ctx.send(f"Successfully removed {name}")
  else:
    logger.info(f"Failed to remove {name}")
    await ctx.send(f"Failed to remove {name}")


@players.command(name='view')
async def view(ctx):
  data = getPlayerIDs()
  encoded_message = "```\n"
  for key, value in data.items():
    encoded_message += f"{key}: {value}\n"
  encoded_message += "```"
  await ctx.send(encoded_message)

async def setup(bot):
    bot.add_command(players)
