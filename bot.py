import discord
import settings

from discord.ext import commands

logger = settings.logging.getLogger("bot")

def run():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
      logger.info(f"User: {bot.user} (ID: {bot.user.id})")

      for cmd_file in settings.CMDS_DIR.glob("*.py"):
        if cmd_file != "__init__.py":
          logger.info(f"loading {cmd_file}")
          await bot.load_extension(f"cmds.{cmd_file.name[:-3]}")
  
    bot.run(settings.DISCORD_API_SECRET, root_logger=True)

if __name__ == "__main__":
    run()

