import logging
import sys

import discord
from discord.ext import commands

from bj import config
from bj import util
from bj import command

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger("BJBot")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="$", intents=intents)

@bot.command()
async def bj(ctx, *args):

    userId = ctx.author.id
    userName = str(ctx.author).split('#')[0]
    args = (None,) if len(args) == 0 else args
    logger.info(f'id: {userId}, name: {userName}, args: {args}')

    ctx.conn = util.initialize(userId, userName)

    # process user command
    cmd = args[0]
    if cmd in ('n', 'new'):
        await command.new(ctx)
    elif cmd in ('j', 'join'):
        await command.join(ctx)
    elif cmd in ('r', 'rank'):
        await command.rank(ctx)
    elif cmd in ('h', 'help'):
        await command.help(ctx)
    else:
        await command.hint(ctx)

bot.run(config.DISCORD_TOKEN)
