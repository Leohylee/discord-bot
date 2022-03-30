import logging
from random import randrange
from os.path import exists
import sqlite3

from . import config

logger = logging.getLogger("BJBot.util")

def initializeEnvironment(bot):
    if not exists(config.DB_FILE_PATH):
        logger.info('sqlite db file not found, creating sqlite db file')
        conn = sqlite3.connect(config.DB_FILE_PATH)

        createPlayersDataSet(conn)
        createLobbyDataSet(conn)
    
    bot.BJ_LOBBY_WAIT_TIME_SECOND = config.BJ_LOBBY_WAIT_TIME_SECOND
    bot.BJ_ROUND_PLAYER_INPUT_WAIT_TIME_SECOND = config.BJ_ROUND_PLAYER_INPUT_WAIT_TIME_SECOND
    bot.BJ_WINNING_POINT = config.BJ_WINNING_POINT

    if not hasattr(bot, 'game_exists'):
        bot.game_exists = False
    if not hasattr(bot, 'allow_join_game'):
        bot.allow_join_game = False
    if not hasattr(bot, 'timer'):
        bot.timer = None
    if not hasattr(bot, 'turn_lock'):
        bot.turn_lock = None

def getNewConnection():
    return sqlite3.connect(config.DB_FILE_PATH)

def initializePlayer(userId, userName):
    conn = sqlite3.connect(config.DB_FILE_PATH)
    addNewPlayer(conn, userId, userName)
    return conn

def _isTableExists(conn, tableName):
    curr = conn.cursor()
    curr.execute(f'select count(name) from sqlite_master where type="table" and name="{tableName}"')
    try:
        return True if curr.fetchone()[0]==1 else False
    finally:
        curr.close()

def isPlayerExists(conn, uesrId):
    curr = conn.cursor()
    curr.execute(f'select count(*) from {config.DB_TABLE_NAME_PLAYER} where userId="{uesrId}"')
    try:
        return True if curr.fetchone()[0]==1 else False
    finally:
        curr.close()

def addNewPlayer(conn, userId, userName):
    if isPlayerExists(conn, userId):
        return
    logger.info(f'user id {userId} not exists in players data, player record will be created')
    sql = (f'insert into {config.DB_TABLE_NAME_PLAYER} (userId, userName) values ("{userId}", "{userName}")')
    _executeDML(conn, sql)

def _isPlayersDataSetExists(conn):
    return _isTableExists(conn, config.DB_TABLE_NAME_PLAYER)

def _isLobbyDataSetExists(conn):
    return _isTableExists(conn, config.DB_CREATE_LOBBY_SQL)

def _executeDDL(conn, sql):
    try:
        curr = conn.cursor()
        curr.execute(sql)
        return curr
    except BaseException as e:
        print(e)

def _executeDML(conn, sql):
    try:
        curr = conn.cursor()
        curr.execute(sql)
        conn.commit()
    except BaseException as e:
        print(e)

def createPlayersDataSet(conn):
    if _isPlayersDataSetExists(conn):
        return
    logger.info('create player table')
    _executeDDL(conn, config.DB_CREATE_PLAYER_SQL)

def createLobbyDataSet(conn):
    if _isLobbyDataSetExists(conn):
        return
    logger.info('create lobby table')
    _executeDDL(conn, config.DB_CREATE_LOBBY_SQL)

def getRankData(conn):
    sql = (f'select * from {config.DB_TABLE_NAME_PLAYER}')
    curr = _executeDDL(conn, sql)
    return curr.fetchall()

def getProperty(ctx, key):
    return getattr(ctx.bot, key)

def getPropertyOrDefault(ctx, key, default):
    if hasattr(ctx.bot, key):
        return getattr(ctx.bot, key)
    else:
        return default

def setProperty(ctx, key, value):
    setattr(ctx.bot, key, value)

def emptyLobby(conn):
    sql = (f'delete from {config.DB_TABLE_NAME_LOBBY}')
    _executeDML(conn, sql)

def joinLobby(conn, userId):
    sql = (f'insert into {config.DB_TABLE_NAME_LOBBY} values ("{userId}")')
    _executeDML(conn, sql)

def listLobby(conn):
    sql = (f'select {config.DB_TABLE_NAME_LOBBY}.userId, userName from {config.DB_TABLE_NAME_LOBBY}, {config.DB_TABLE_NAME_PLAYER} where {config.DB_TABLE_NAME_LOBBY}.userId = {config.DB_TABLE_NAME_PLAYER}.userId')
    curr = _executeDDL(conn, sql)
    return curr.fetchall()

def formatBalance(amount):
    return '${:0,.0f}'.format(amount).replace('$-','-$')

def drawCard(deck):
    pos = randrange(0, len(deck))
    draw = deck[pos]
    deck = deck.replace(deck[pos], '', 1)
    return (draw, deck)

def showRoundInfo(ctx, round, host, players):
    output = f'**Round {round}**\n'
    output += f"* * * * * *** Host ***: {', '.join(host['deck'])} * * * * *\n"
    for i in range(len(players)):
         output += f"@{players[i]['userName']}: {', '.join(players[i]['deck'])} {calcPoints(ctx, players[i]['deck'])}\n"
    return output

def calcPoints(ctx, deck):
    count_A = deck.count('A')
    count_10 = (deck.count('J') + deck.count('Q') + deck.count('K'))*10
    sum_rest = sum([int(card) for card in deck.replace('A','').replace('J','').replace('Q','').replace('K','')]) + count_10

    combination_A = []
    for i in range(0, count_A + 1):
        combination_A.append(i * 11 + (count_A - i) * 1)
    calculated = [combination+sum_rest for combination in combination_A]
    if getProperty(ctx, 'BJ_WINNING_POINT') in calculated:
        return [getProperty(ctx, 'BJ_WINNING_POINT')]
    else:
        return calculated
