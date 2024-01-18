import settings

from damageGetter import getDamage
from discord.ext import commands
from playerIDs import getPlayerIDs

logger = settings.logging.getLogger("bot")


@commands.group()
async def dmg(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("try !help dmg")


# This command should check the damage of the player that called it.
@dmg.command(name="check")
async def check(ctx, match_count=1):
    """Checks your damage from your most recent match."""

    logger.info(f"{ctx.author} called !dmg check")
    await ctx.send("Inspecting the damage...")
    if ctx.author.name not in getPlayerIDs():
        logger.error(f"{ctx.author.name} not in file")
        await ctx.send(
            f"I'm sorry {ctx.author.nick}, whoever wrote this code forgot about you..."
        )
    else:
        await ctx.send(getDamage(ctx.author, match_count))


# This command should compare the damage between players of the caller's most recent match
@dmg.command(name="compare")
async def compare(ctx):
    """Compares your damage between players of your most recent match."""

    await ctx.send("Not implemented yet")


async def setup(bot):
    bot.add_command(dmg)
