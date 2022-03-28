import logging
import sys

import discord
from discord.ext import commands

from bj import config, util, command

logging.basicConfig(stream=sys.stdout,
level=logging.INFO,
format='%(asctime)s.%(msecs)03d %(name)s %(processName)s %(threadName)s [%(levelname)s] %(message)s',
datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger("BJBot")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="$", intents=intents)

util.initializeEnvironment()

@bot.command()
async def bj(ctx, *args):

    ctx.userId = ctx.author.id
    ctx.userName = str(ctx.author).split('#')[0]
    ctx.args = ('hint',) if len(args) == 0 else args
    logger.info(f'id: {ctx.userId}, name: {ctx.userName}, args: {ctx.args}')

    ctx.conn = util.initializePlayer(ctx.userId, ctx.userName)

    # process user command
    cmd = ctx.args[0]
    if cmd in ('n', 'new'):
        await command.new(ctx)
    elif cmd in ('j', 'join'):
        await command.join(ctx)
    elif cmd in ('r', 'rank'):
        await command.rank(ctx)
    elif cmd in ('h', 'help'):
        await command.help(ctx)
    elif cmd in ('test'):
        await command.test(ctx)
    else:
        await command.hint(ctx)
    
    ctx.conn.close()

bot.run(config.DISCORD_TOKEN)
