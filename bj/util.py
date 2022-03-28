import logging
from os.path import exists
import sqlite3

from . import config

logger = logging.getLogger("BJBot.util")

def initializeEnvironment():
    if not exists(config.DB_FILE_PATH):
        logger.info('sqlite db file not found, creating sqlite db file')
        conn = sqlite3.connect(config.DB_FILE_PATH)

        createPlayersDataSet(conn)
        createLobbyDataSet(conn)
        createPropertiesDataSet(conn)

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

def isGameExists(conn):
    return _isTableExists(conn, config.DB_TABLE_NAME_GAME)

def _isPlayersDataSetExists(conn):
    return _isTableExists(conn, config.DB_TABLE_NAME_PLAYER)

def _isLobbyDataSetExists(conn):
    return _isTableExists(conn, config.DB_CREATE_LOBBY_SQL)

def _isPropertiesDataSetExists(conn):
    return _isTableExists(conn, config.DB_TABLE_NAME_PROPERTIES)

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

def createGame(conn):
    logger.info('create game table')
    _executeDDL(conn, config.DB_CREATE_TABLE_SQL)

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

def createPropertiesDataSet(conn):
    if _isPropertiesDataSetExists(conn):
        return
    logger.info('create properties table')
    _executeDDL(conn, config.DB_CREATE_PROPERTIES_SQL)
    _initializePropertiesDataSet(conn)

def _initializePropertiesDataSet(conn):
    logger.info('initializing properties table')
    _executeDML(conn, config.DB_INSERT_PROPERTIES_SQL)

def getRankData(conn):
    sql = (f'select * from {config.DB_TABLE_NAME_PLAYER}')
    curr = _executeDDL(conn, sql)
    return curr.fetchall()

def getProperty(conn, key):
    sql = (f'select value from {config.DB_TABLE_NAME_PROPERTIES} where key = "{key}"')
    curr = _executeDDL(conn, sql)
    return curr.fetchone()[0]

def updateProperty(conn, key, value):
    sql = (f'update {config.DB_TABLE_NAME_PROPERTIES} set value = "{value}" where key = "{key}"')
    logger.info(f'updateProperty {key} {value}')
    _executeDML(conn, sql)

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
