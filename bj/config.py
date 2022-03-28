import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("BJ_BOT_TOKEN")
DB_FILE_NAME = 'discord-bot.sqlite'
DB_FILE_PATH = Path(os.getenv("temp")).joinpath(DB_FILE_NAME)
DB_TABLE_NAME_GAME = 'bj_game'
DB_TABLE_NAME_PLAYER = 'bj_players'
DB_TABLE_NAME_PROPERTIES = 'bj_properties'
DB_FIELD_ALLOW_JOIN_GAME = 'allowJoinGame'
DB_CREATE_TABLE_SQL = (f'''create table if not exists {DB_TABLE_NAME_GAME} (
	userId VARCHAR(255) PRIMARY KEY,
    userName VARCHAR(255) NOT NULL,
	card VARCHAR(52) NOT NULL,
    point INTEGER NOT NULL
); ''')
DB_CREATE_PLAYER_SQL = (f'''create table if not exists {DB_TABLE_NAME_PLAYER} (
	userId VARCHAR(255) PRIMARY KEY,
    userName VARCHAR(255) NOT NULL,
    credit INTEGER NOT NULL DEFAULT(1000000)
); ''')
DB_CREATE_PROPERTIES_SQL = (f'''create table if not exists {DB_TABLE_NAME_PROPERTIES} (
	key VARCHAR(255) PRIMARY KEY,
    value VARCHAR(255) NOT NULL
); ''')
DB_INSERT_PROPERTIES_SQL = (f'''insert into {DB_TABLE_NAME_PROPERTIES} values
('{DB_FIELD_ALLOW_JOIN_GAME}', 'False')
; ''')
CARD='123456789AKQJ123456789AKQJ123456789AKQJ123456789AKQJ123456789AKQJ123456789AKQJ123456789AKQJ123456789AKQJ'

BJ_LOBBY_WAIT_TIME_SECOND=30