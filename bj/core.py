import threading
import time
from . import util
from . import config

def lobbyWaiting(second):
    conn = util.getNewConnection()
    util.updateProperty(conn, config.DB_FIELD_ALLOW_JOIN_GAME, str(True))
    time.sleep(second)
    util.updateProperty(conn, config.DB_FIELD_ALLOW_JOIN_GAME, str(False))

async def newGame(ctx):
    if util.isGameExists(ctx.conn):
        msg = 'There is active game running, please wait for next round'
        await ctx.channel.send(msg)
    else:
        msg = f'⭐⭐⭐New game created, {config.BJ_LOBBY_WAIT_TIME_SECOND}s to join⭐⭐⭐'
        await ctx.channel.send(msg)

        t = threading.Thread(target=lobbyWaiting, args=(int(config.BJ_LOBBY_WAIT_TIME_SECOND),))
        t.start()

    # sql = (f'select * from {config.DB_TABLE_NAME_PLAYER}')
    # curr = util._executeDDL(ctx.conn, sql)
    # return curr.fetchall()

async def joinGame(ctx):
    if not (util.getProperty(ctx.conn, config.DB_FIELD_ALLOW_JOIN_GAME).lower() == str(True).lower()):
        msg = f"can't join game at the moment"
        await ctx.channel.send(msg)
    else:
        msg = f"{ctx.userName} joined"
        await ctx.channel.send(msg)
