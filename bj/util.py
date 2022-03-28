import os
from os.path import exists
from pathlib import Path
import sqlite3

from . import config

def initialize(userId, userName):
    dbPath = Path(os.getenv('temp')).joinpath(config.DB_FILE_NAME)

    if not exists(dbPath):
        print ('sqlite db file not found, sqlite db file will be created')
    conn = sqlite3.connect(dbPath)

    if not _isPlayerDataSetExists(conn):
        createPlayerData(conn)
    
    if not isPlayerExists(conn, userId):
        print (f'user id {userId} not exists in players data, player record will be created')
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

def addNewPlayer(conn, uesrId, userName):
    sql = (f'insert into {config.DB_TABLE_NAME_PLAYER} (userId, userName) values ("{uesrId}", "{userName}")')
    _executeDML(conn, sql)

def isGameExists(conn):
    return _isTableExists(conn, config.DB_TABLE_NAME_GAME)

def _isPlayerDataSetExists(conn):
    return _isTableExists(conn, config.DB_TABLE_NAME_PLAYER)

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
    print ('create game table ... ', end='')
    _executeDDL(conn, config.DB_CREATE_TABLE_SQL)
    print ('done')

def createPlayerData(conn):
    print ('create player table ... ', end='')
    _executeDDL(conn, config.DB_CREATE_PLAYER_SQL)
    print ('done')

def getRankData(conn):
    sql = (f'select * from {config.DB_TABLE_NAME_PLAYER}')
    curr = _executeDDL(conn, sql)
    return curr.fetchall()
