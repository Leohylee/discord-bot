import logging
import os
import sys
import asyncio

from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from discord.ext import commands


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger("PA Bot")
logger.setLevel(logging.INFO)

load_dotenv()

DISCORD_TOKEN = os.getenv("PA_BOT_TOKEN")

# intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!")

@bot.command()
async def remindme(ctx, time):
    def convert_time(time):
        pos = ['s', 'm', 'h', 'd']
        time_dict = {"s": 1, "m": 60, "h": 3600, "d": 3600*24}
        time_concat = ""
        seconds = 0
        for num in time:
            if num in pos and time_concat.isnumeric():
                seconds = seconds + time_dict[num] * int(time_concat)
                time_concat = ""
            else:
                time_concat = time_concat + num
        return seconds

    if ctx.message.reference:
        creater = "<@%s>" % str(ctx.author.id)
        message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        message_date = message.created_at.replace(tzinfo=timezone.utc, microsecond=0).astimezone(tz=None)
        author = "<@%s>" % str(message.author.id)
        seconds = convert_time(time)
        await ctx.channel.send("I will remind you this message on %s" % (datetime.now() + timedelta(0, int(seconds))).replace(microsecond=0))
        await asyncio.sleep(seconds)
        await ctx.channel.send("%s Reminder: ''%s'' -- by %s at %s" % (creater, message.content, author, str(message_date)))
    else:
        await ctx.channel.send("Please make reference to a message for reminder.")

bot.run(DISCORD_TOKEN)