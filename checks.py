import settings
import discord
from discord.ext import commands

logger = settings.logging.getLogger("bot")

async def is_owner(ctx):
  return False #ctx.author.id == ctx.guild.owner_id
  