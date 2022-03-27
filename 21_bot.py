import logging
import os
import sys

import discord
from discord.ext import commands
from dotenv import load_dotenv

from bj.util import *
from bj.core import *
from bj.command import *

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger("Reply Bot")
logger.setLevel(logging.INFO)

load_dotenv()

DISCORD_TOKEN = os.getenv("BJ_BOT_TOKEN")
CAT_API_TOKEN = os.getenv("CAT_API_TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="$", intents=intents)

@bot.command()
async def bj(ctx, *args):

    userId = ctx.author.id
    userName = str(ctx.author).split('#')[0]
    args = (None,) if len(args) == 0 else args
    print (userId, userName, args)


    conn = initialize(userId, userName)


    async def showUserHint():
        if not isGameExists(conn):
            msg = (f'No game at the moment, use "$bj new" to create new game')
        else:
            # TODO: check if user in game to prompt hints
            msg = (f'use "$bj join" to join')
        return msg


    # process user command
    cmd = args[0]
    match cmd:
        case 'new':
            # TODO: create new game
            pass
        case 'join':
            # TODO: join / enqueue game
            pass
        case 'rank':
            msg = rank(conn)
        case 'test':
            msg = (f"<@{userId}> It's your turn! (t: take a new card, s: skip) ")
        case _:
            msg = await showUserHint()

    await ctx.channel.send(msg)


bot.run(DISCORD_TOKEN)
