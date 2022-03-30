from . import util, core, config

async def help(ctx):
    msg = f"""
{'$bj [h|help]': <20} show help
{'$bj [n|new]': <20}  new game
{'$bj [j|join]': <20} join game
{'$bj [r|rank]': <20} show leaderboard
    """
    await ctx.channel.send(msg)

async def hint(ctx):
    if not util.getProperty(ctx, 'game_exists'):
        await ctx.channel.send(config.BJ_MSG['HINT_NEW_GAME'])
    else:
        await ctx.channel.send(config.BJ_MSG['HINT_JOIN_GAME'])

async def rank(ctx):
    data = util.getRankData(ctx.conn)
    output = config.BJ_MSG['LEADERBOARD_HEADLINE']
    for userId, userName, credit in data:
        balance = util.formatBalance(float(credit))
        output += (f'{userName}:\t{balance}\n')
    await ctx.channel.send(output)

async def new(ctx):
    await core.newGame(ctx)

async def join(ctx):
    await core.joinGame(ctx)
