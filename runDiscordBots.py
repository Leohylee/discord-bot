import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from cogs.pa_cog import PaCog
from cogs.reply_cog import ReplyCog

load_dotenv()
REPLY_BOT_TOKEN = os.getenv("REPLY_BOT_TOKEN")
CAT_API_TOKEN = os.getenv("CAT_API_TOKEN")

intents = discord.Intents.all()
reply_bot = commands.Bot(command_prefix="!", intents=intents)
reply_bot.add_cog(ReplyCog(reply_bot, CAT_API_TOKEN))
reply_bot.add_cog(PaCog(reply_bot))
reply_bot.run(REPLY_BOT_TOKEN)