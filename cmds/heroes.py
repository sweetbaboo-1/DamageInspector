import settings
from discord.ext import commands
from heroIDs import addHero, removeHero, getHeroData
from checks import is_owner

logger = settings.logging.getLogger("bot")


@commands.group()
async def heroes(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("try !help heroes")


# This command should add a hero to the json file
@heroes.command(name="add")
@commands.check(is_owner)
async def add(ctx, id: int, *name: str):
    """{id, name}"""
    heroName = " ".join(name)
    logger.info("Trying to add hero")
    await ctx.send(f"Adding hero {heroName} with id {id}.")
    if addHero(id, heroName):
        logger.info(f"Added {name} with id {id}")
        await ctx.send(f"Successfully added {heroName}.")
    else:
        logger.info(f"Failed to add {name} with id {id}")
        await ctx.send(f"Failed to add {heroName}.")


# This command should remove a hero from the json file
@heroes.command(name="remove")
@commands.check(is_owner)
async def remove(ctx, *name: str):
    """{name}"""
    heroName = " ".join(name)
    await ctx.send(f"Removing hero {heroName}.")
    if removeHero(heroName):
        logger.info(f"Removed {name}")
        await ctx.send(f"Successfully removed {heroName}.")
    else:
        logger.info(f"Failed to remove {name}")
        await ctx.send(f"Failed to remove {heroName}.")


@heroes.command(name="view")
@commands.check(is_owner)
async def view(ctx):
    data = getHeroData()
    encoded_message = "```\n"
    for key, value in data.items():
        encoded_message += f"{key}: {value}\n"
    encoded_message += "```"
    await ctx.send(encoded_message)


async def setup(bot):
    bot.add_command(heroes)
