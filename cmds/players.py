import discord
import settings
from discord.ext import commands
from playerIDs import addPlayer, removePlayer, getPlayerIDs
from checks import is_owner

logger = settings.logging.getLogger("bot")


@commands.group()
async def players(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("try !help players")


# This command should add a player to the json file
@players.command(name="addPlayer")
@commands.check(is_owner)
async def addPlayerID(ctx, member: discord.Member, id: int):
    """{@player, id}"""

    name = member.name
    logger.info("Trying to add player")
    await ctx.send(f"Adding player {name} with id {id}.")
    if addPlayer(name, id):
        logger.info(f"Added {name} with id {id}")
        await ctx.send(f"Successfully added {name}.")
    else:
        logger.info(f"Failed to add {name} with id {id}.")
        await ctx.send(f"Failed to add {name}")


# This command should add a player to the json file
@players.command(name="add")
async def add(ctx, id: int = -1):
    """Add yourself {id}"""

    if id < 0:
        await ctx.send(f"You must include your OpenDotA ID")
        return

    name = ctx.author.name
    logger.info("Trying to add player")
    await ctx.send(f"Adding player {name} with id {id}.")
    if addPlayer(name, id):
        logger.info(f"Added {name} with id {id}")
        await ctx.send(f"Successfully added {name}.")
    else:
        logger.info(f"Failed to add {name} with id {id}.")
        await ctx.send(f"Failed to add {name}")


# This command should remove a hero from the json file
@players.command(name="removePlayer")
@commands.check(is_owner)
async def removePlayerID(ctx, member: discord.Member):
    """{name}"""

    name = member.name
    await ctx.send(f"Removing player {name}")
    if removePlayer(name):
        logger.info(f"Removed {name}")
        await ctx.send(f"Successfully removed {name}.")
    else:
        logger.info(f"Failed to remove {name}")
        await ctx.send(f"Failed to remove {name}.")


# This command should remove a hero from the json file
@players.command(name="remove")
async def remove(ctx):
    """Remove yourself"""

    name = ctx.author.name
    await ctx.send(f"Removing player {name}")
    name = ctx.author.name
    if removePlayer(name):
        logger.info(f"Removed {name}")
        await ctx.send(f"Successfully removed {name}.")
    else:
        logger.info(f"Failed to remove {name}")
        await ctx.send(f"Failed to remove {name}.")


@players.command(name="view")
async def view(ctx):
    data = getPlayerIDs()
    encoded_message = "```\n"
    for key, value in data.items():
        encoded_message += f"{key}: {value}\n"
    encoded_message += "```"
    await ctx.send(encoded_message)


async def setup(bot):
    bot.add_command(players)
