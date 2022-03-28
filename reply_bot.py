import asyncio
import datetime
import logging
import os
import random
import sys

import discord
import requests
from discord.ext import commands
from dotenv import load_dotenv

from modules.replies import Replies

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger("Reply Bot")
logger.setLevel(logging.INFO)

load_dotenv()

DISCORD_TOKEN = os.getenv("REPLY_BOT_TOKEN")
CAT_API_TOKEN = os.getenv("CAT_API_TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)


def choose_reply_message(message):
    def translate_time_to_chinese_greet(h):
        return "早安" if 5 <= h <= 11 else "午安" if 12 <= h <= 17 else "晚安"

    def call_cat_api():
        url = "https://api.thecatapi.com/v1/images/search?mime_types=gif"
        querystring = {"Connection": "close"}
        headers = {"x-api-key": CAT_API_TOKEN}
        response = requests.request("GET", url, headers=headers, params=querystring)
        if response and response.status_code == 200:
            data = response.json()
            if data and data[0] and data[0].get("url"):
                return data[0].get("url")

    reply_type = ["greetings", "do_you_know", "cat"]
    weights = [60, 20, 20]
    bot_replies = Replies()
    reply = "hi auntie!"

    if message.content.lower() in bot_replies.greetings:
        chosen = random.choices(reply_type, weights)[0]
        match chosen:
            case "greetings":
                reply = random.choice(bot_replies.greetings) + "!"
            case "do_you_know":
                reply = random.choice(bot_replies.do_you_know).replace("_", translate_time_to_chinese_greet(datetime.datetime.now().hour)) + "\n" + random.choice(bot_replies.flowers)
            case "cat":
                reply = call_cat_api()
        return reply, chosen
    elif message.content.lower() in ["cs?", "play?", "csgo?"]:
        return random.choice(bot_replies.csgo), "csgo"
    elif message.content.lower() in ["on9","diu","dllm","pk","jm9","on99","diu nei","仆街","屌","屌你","fuck","fuck you","fuck u","fk","damn"]:
        return random.choice(bot_replies.anti_swear), "anti_swear"
    elif message.content.lower() == "笑左":
        return "笑埋右", "laugh_right"
    elif message.content.lower() == ".":
        return "ヽ( ._. )ノ", ". emoji"
    else:
        return "", "unknown"


@bot.event
async def on_message(message):
    """EVENT LISTENER FOR WHEN A NEW MESSAGE IS SENT TO A CHANNEL."""
    if message.author == bot.user:
        return
    author = str(message.author.name)
    guild = str(message.author.guild)
    reply, reply_type = choose_reply_message(message)
    if reply_type != "unknown":
        # SENDS BACK A MESSAGE TO THE CHANNEL.
        await message.channel.send(reply)
        logger.info("%s: %s (%s) on_message - %s", str(datetime.datetime.now()), author, guild, reply_type)
    else:
        await bot.process_commands(message)


@bot.command()
async def remindme(ctx, time):
    def convert_time(time):
        time_dict = {"s": 1, "m": 60, "h": 3600, "d": 3600 * 24}
        time_concat = ""
        wait_time = 0
        for num in time:
            if num in time_dict and time_concat.isnumeric():
                wait_time = wait_time + time_dict[num] * int(time_concat)
                time_concat = ""
            else:
                time_concat = time_concat + num
        return wait_time

    if ctx.message.reference:
        creater = "<@%s>" % str(ctx.author.id)
        message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        message_date = message.created_at.replace(tzinfo=datetime.timezone.utc, microsecond=0).astimezone(tz=None)
        author = "<@%s>" % str(message.author.id)
        seconds = convert_time(time)
        await ctx.channel.send("I will remind you this message on %s" % (datetime.datetime.now() + datetime.timedelta(0, int(seconds))).replace(microsecond=0))
        await asyncio.sleep(seconds)
        await ctx.channel.send("%s Reminder: ''%s'' -- by %s at %s" % (creater, message.content, author, str(message_date)))
    else:
        await ctx.channel.send("Please make reference to a message for reminder.")


@bot.event
async def on_member_update(before, after):
    if before.status != after.status:
        logger.info("%s: %s (%s) - %s -> %s", str(datetime.datetime.now()), str(after.name), str(after.guild.name), str(before.status), str(after.status))

bot.run(DISCORD_TOKEN)
