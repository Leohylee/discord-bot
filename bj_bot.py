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
bot.BJ_LOBBY_WAIT_TIME_SECOND = config.BJ_LOBBY_WAIT_TIME_SECOND

@bot.command()
async def bj(ctx, *args):

    ctx.userId = ctx.author.id
    ctx.userName = str(ctx.author).split('#')[0]
    ctx.args = ('hint',) if len(args) == 0 else args
    logger.info(f'id: {ctx.userId}, name: {ctx.userName}, args: {ctx.args}')

    ctx.conn = util.initializePlayer(ctx.userId, ctx.userName)

    if not hasattr(bot, 'allow_join_game'):
        bot.allow_join_game = False

    if not hasattr(bot, 'timer'):
        bot.timer = None

    if not hasattr(bot, 'turn_lock'):
        bot.turn_lock = None
    
    ctx.bot = bot

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
    elif cmd in ('t', 'take', 's', 'stand'):
        if (str(ctx.userId) == bot.turn_lock):
            if cmd in ('t', 'take'):
                logger.info('a take action sent from ' + str(ctx.userId) + ' ' + ctx.userName)
                bot.stopTimer.set_result('take')
            else:
                logger.info('a stand action sent from ' + str(ctx.userId) + ' ' + ctx.userName)
                bot.stopTimer.set_result('stand')
    elif cmd in ('update_config'):
        util.setProperty(ctx, ctx.args[1], ctx.args[2])
    else:
        await command.hint(ctx)
    
    ctx.conn.close()

bot.run(config.DISCORD_TOKEN)

