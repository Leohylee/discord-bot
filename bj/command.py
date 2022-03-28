from . import util
from . import core

async def help(ctx):
    msg = f"""
{'$bj [h|help]': <20} show help
{'$bj [n|new]': <20} create new game
{'$bj [j|join]': <20} join game
{'$bj [r|rank]': <20} show leaderboard
    """
    await ctx.channel.send(msg)

async def hint(ctx):
    if not util.isGameExists(ctx.conn):
        msg = (f'No game at the moment, use "$bj new" to create new game')
    else:
        # TODO: check if user in game to prompt hints
        msg = (f'use "$bj join" to join')
    await ctx.channel.send(msg)

async def rank(ctx):
    data = util.getRankData(ctx.conn)
    output = '🏆🏆🏆 leaderboard (credit) 🏆🏆🏆\n'
    for row in data:
        balance = '${:0,.0f}'.format(float(row[2])).replace('$-','-$')
        output += (f'{row[1]}:\t{balance}\n')
    await ctx.channel.send(output)

async def new(ctx):
    core.newGame(ctx)
    return

async def join(ctx):
    core.joinGame(ctx)
    return