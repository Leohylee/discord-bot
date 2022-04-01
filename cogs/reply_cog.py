import datetime
import logging
import random
import sys

import requests
from discord.ext import commands

from modules.replies import Replies
from modules.user_messages import User_Messages

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger("Reply Bot")
logger.setLevel(logging.INFO)


class ReplyCog(commands.Cog):
    CAT_API_TOKEN = ""

    def __init__(self, bot, CAT_API_TOKEN):
        self.bot = bot
        self.CAT_API_TOKEN = CAT_API_TOKEN

    def choose_reply_message(self, message):
        def translate_time_to_chinese_greet(h):
            return "早安" if 5 <= h <= 11 else "午安" if 12 <= h <= 17 else "晚安"

        def call_cat_api():
            url = "https://api.thecatapi.com/v1/images/search?mime_types=gif"
            querystring = {"Connection": "close"}
            headers = {"x-api-key": self.CAT_API_TOKEN}
            response = requests.request("GET", url, headers=headers, params=querystring)
            if response and response.status_code == 200:
                data = response.json()
                if data and data[0] and data[0].get("url"):
                    return data[0].get("url")

        bot_replies = Replies()
        user_messages = User_Messages()
        reply = "hi!"

        if message.content.lower() in bot_replies.greetings:
            chosen = random.choices(Replies.greeting_reply_type, Replies.greeting_weights)[0]
            match chosen:
                case "greetings":
                    reply = random.choice(bot_replies.greetings) + "!"
                case "do_you_know":
                    reply = random.choice(bot_replies.do_you_know).replace("_", translate_time_to_chinese_greet(
                        datetime.datetime.now().hour)) + "\n" + random.choice(bot_replies.flowers)
                case "cat":
                    reply = call_cat_api()
            return reply, chosen
        elif message.content.lower() in user_messages.csgo:
            return random.choice(bot_replies.csgo), "csgo"
        elif message.content.lower() in user_messages.swear:
            return random.choice(bot_replies.anti_swear), "anti_swear"
        elif message.content.lower() in user_messages.dot:
            return random.choice(bot_replies.dot), ". emoji"
        else:
            return "", "unknown"

    @commands.Cog.listener()
    async def on_message(self, message):
        """EVENT LISTENER FOR WHEN A NEW MESSAGE IS SENT TO A CHANNEL."""
        if message.author == self.bot.user:
            return
        author = str(message.author.name)
        guild = str(message.author.guild)
        reply, reply_type = self.choose_reply_message(message)
        if reply_type != "unknown":
            # SENDS BACK A MESSAGE TO THE CHANNEL.
            await message.channel.send(reply)
            logger.info("%s: %s (%s) on_message - %s", str(datetime.datetime.now()), author, guild, reply_type)
        else:
            await self.bot.process_commands(message)


def setup(bot):
    bot.add_cog(ReplyCog(bot))
