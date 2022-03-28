import asyncio

from . import util, config

async def lobbyWaiting(ctx, second):
    conn = util.getNewConnection()
    util.updateProperty(conn, config.DB_FIELD_ALLOW_JOIN_GAME, str(True))
    await joinGame(ctx)
    await asyncio.sleep(second)
    util.updateProperty(conn, config.DB_FIELD_ALLOW_JOIN_GAME, str(False))
    await ctx.channel.send(config.BJ_MSG['LOBBY_CLOSED'])

async def newGame(ctx):
    if util.isGameExists(ctx.conn):
        await ctx.channel.send(config.BJ_MSG['GAME_EXISTS_WAIT_FOR_NEXT_ROUND'])
    else:
        await ctx.channel.send(config.BJ_MSG['NEW_GAME_CREATED'])

        util.emptyLobby(ctx.conn)
        await lobbyWaiting(ctx, int(config.BJ_LOBBY_WAIT_TIME_SECOND))

        players = util.listLobby(ctx.conn)
        output = config.BJ_MSG['GAME_START_HEADLINE']
        for userId, userName in players:
            output += f'<@{userId}> '
        await ctx.channel.send(output)

async def joinGame(ctx):
    if not (util.getProperty(ctx.conn, config.DB_FIELD_ALLOW_JOIN_GAME).lower() == str(True).lower()):
        await ctx.channel.send(config.BJ_MSG['JOIN_GAME_NOT_AVAILALBE'])
    else:
        util.joinLobby(ctx.conn, ctx.userId)
        players = util.listLobby(ctx.conn)
        output = config.BJ_MSG['JOINED_PLAYERS']
        for userId, userName in players:
            output += f'@{userName} '
        await ctx.channel.send(output)
