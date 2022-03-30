import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("BJ_BOT_TOKEN")
DB_FILE_NAME = 'discord-bot.sqlite'
DB_FILE_PATH = Path(os.getenv("temp")).joinpath(DB_FILE_NAME)
DB_TABLE_NAME_PLAYER = 'bj_players'
DB_TABLE_NAME_LOBBY = 'bj_lobby'
DB_CREATE_PLAYER_SQL = (f'''create table if not exists {DB_TABLE_NAME_PLAYER} (
	userId VARCHAR(255) PRIMARY KEY,
    userName VARCHAR(255) NOT NULL,
    credit INTEGER NOT NULL DEFAULT(1000000)
); ''')
DB_CREATE_LOBBY_SQL = (f'''create table if not exists {DB_TABLE_NAME_LOBBY} (
	userId VARCHAR(255) PRIMARY KEY
); ''')

BJ_DECK='123456789AKQJ123456789AKQJ123456789AKQJ123456789AKQJ123456789AKQJ123456789AKQJ123456789AKQJ123456789AKQJ'
BJ_WINNING_POINT=21
BJ_LOBBY_WAIT_TIME_SECOND=30
BJ_ROUND_PLAYER_INPUT_WAIT_TIME_SECOND=60

BJ_MSG_EN = {
    'GAME_EXISTS_WAIT_FOR_NEXT_ROUND': 'please wait for game end',
    'NEW_GAME_CREATED': '⭐⭐⭐ New game created, %s second to join ⭐⭐⭐',
    'JOIN_GAME_NOT_AVAILALBE': 'please wait for new game',
    'HINT_NEW_GAME': 'No game at the moment, use "$bj new" to create new game',
    'HINT_JOIN_GAME': 'use "$bj join" to join',
    'LEADERBOARD_HEADLINE': '🏆🏆🏆 leaderboard (credit) 🏆🏆🏆\n',
    'LOBBY_CLOSED': '🔒 lobby closed',
    'GAME_START_HEADLINE': '🎮 Game Start\n',
    'JOINED_PLAYERS': 'Joined players:\n',
    'GAME_END_HEADLINE': '🎉🎉🎉 Game End 🎉🎉🎉'
}
BJ_MSG = BJ_MSG_EN
