from . import util
from . import config

def newGame(ctx):
    if util.isGameExists(ctx.conn):
        msg = 'There is active game running, please wait for next round'
        ctx.channel.send(msg)
    else:
        pass
    sql = (f'select * from {config.DB_TABLE_NAME_PLAYER}')
    curr = util._executeDDL(ctx.conn, sql)
    return curr.fetchall()

def joinGame(ctx):
    pass