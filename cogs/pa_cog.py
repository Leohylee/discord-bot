import asyncio
import logging
import sys
from datetime import datetime, timezone, timedelta

import requests
from discord.ext import commands

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger("PA Bot")
logger.setLevel(logging.INFO)


class PaCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def remindme(self, ctx, time):
        def convert_time(time):
            pos = ['s', 'm', 'h', 'd']
            time_dict = {"s": 1, "m": 60, "h": 3600, "d": 3600 * 24}
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
            await ctx.channel.send("I will remind you this message on %s" % (
                    datetime.now() + timedelta(0, int(seconds))).replace(microsecond=0))
            await asyncio.sleep(seconds)
            await ctx.channel.send(
                "%s Reminder: ''%s'' -- by %s at %s" % (creater, message.content, author, str(message_date)))
        else:
            await ctx.channel.send("Please make reference to a message for reminder.")

    @commands.command()
    async def steamsales(self, ctx):
        url = "https://store.steampowered.com/api/featuredcategories"
        querystring = {"Connection": "close"}
        response = requests.request("GET", url, params=querystring)
        if response and response.status_code == 200:
            data = response.json()
            if data and data.get("specials"):
                games = ["Steam Sales:"]
                for item in data.get("specials").get("items"):
                    games.append("%s: $%s -> $%s (until %s)" % (
                        item.get("name"), item.get("original_price") / 100, item.get("final_price") / 100,
                        datetime.fromtimestamp(item.get("discount_expiration"))))
                await ctx.channel.send("\n".join(games))

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.status != after.status:
            logger.info("%s: %s (%s) - %s -> %s", str(datetime.now()), str(after.name), str(after.guild.name),
                        str(before.status), str(after.status))


def setup(bot):
    bot.add_cog(PaCog(bot))
