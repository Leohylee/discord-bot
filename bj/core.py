import logging
import asyncio
from concurrent.futures import FIRST_COMPLETED

from . import util, config

logger = logging.getLogger("BJBot.core")

async def lobbyWaiting(ctx, second):
    conn = util.getNewConnection()
    util.setProperty(ctx, 'allow_join_game', True)
    await joinGame(ctx)
    await asyncio.sleep(second)
    util.setProperty(ctx, 'allow_join_game', False)
    await ctx.channel.send(config.BJ_MSG['LOBBY_CLOSED'])

async def newGame(ctx):
    if util.isGameExists(ctx.conn):
        await ctx.channel.send(config.BJ_MSG['GAME_EXISTS_WAIT_FOR_NEXT_ROUND'])
    else:
        await ctx.channel.send(config.BJ_MSG['NEW_GAME_CREATED'] % str(util.getProperty(ctx, 'BJ_LOBBY_WAIT_TIME_SECOND')))

        util.emptyLobby(ctx.conn)
        await lobbyWaiting(ctx, int(util.getProperty(ctx, 'BJ_LOBBY_WAIT_TIME_SECOND')))

        players = util.listLobby(ctx.conn)
        output = config.BJ_MSG['GAME_START_HEADLINE']
        for userId, userName in players:
            output += f'<@{userId}> '
        await ctx.channel.send(output)

        await gameStart(ctx, players)


async def joinGame(ctx):
    if not util.getProperty(ctx, 'allow_join_game'):
        await ctx.channel.send(config.BJ_MSG['JOIN_GAME_NOT_AVAILALBE'])
    else:
        util.joinLobby(ctx.conn, ctx.userId)
        players = util.listLobby(ctx.conn)
        output = config.BJ_MSG['JOINED_PLAYERS']
        for userId, userName in players:
            output += f'@{userName} '
        await ctx.channel.send(output)

async def gameStart(ctx, players_data):
    round = 1
    deck = config.BJ_DECK

    player_deck = ''
    drawCard, deck = util.drawCard(deck)
    player_deck += drawCard
    drawCard, deck = util.drawCard(deck)
    player_deck += drawCard
    host = { 'deck': player_deck, 'stand': False }

    players = []
    for userId, userName in players_data:
        player_deck = ''
        drawCard, deck = util.drawCard(deck)
        player_deck += drawCard
        drawCard, deck = util.drawCard(deck)
        player_deck += drawCard
        players.append( { 'userId': userId, 'userName': userName, 'deck': player_deck, 'stand': False } )
    
    # players.append( { 'userId': 'testID', 'userName': 'testName', 'deck': 'XX', 'stand': True } )

    logger.info(players)

    while round <= 5:
        for roundPlayerIdx in range(len(players)):
            if players[roundPlayerIdx]['stand']:
                continue
            output = f'**Round {round}**\n'
            output += f"* * * * * *** Host ***: {', '.join(host['deck'])} * * * * *\n"
            output += util.listPlayersDeck(players)
            output += f"<@{players[roundPlayerIdx]['userId']}> It's your turn. (t: take, s: stand)"

            ctx.bot.turn_lock = players[roundPlayerIdx]['userId']
            logger.info('round lock released to ' + str(players[roundPlayerIdx]['userId']) + ' ' + players[roundPlayerIdx]['userName'])
            await ctx.channel.send(output)

            count_timer = asyncio.sleep(15)
            stop_future = asyncio.Future()
            ctx.bot.stopTimer = stop_future

            finished, unfinished = await asyncio.wait([count_timer, stop_future], return_when=FIRST_COMPLETED)
            ctx.bot.turn_lock = None
            logger.info('round lock has reset')

            for x in finished:
                roundAction = x.result()
                logger.info(f"{players[roundPlayerIdx]['userId']} {players[roundPlayerIdx]['userName']} round action: {str(roundAction)}")
                if roundAction == 'take':
                    logger.info('a take action received from ' + str(players[roundPlayerIdx]['userId']) + ' ' + players[roundPlayerIdx]['userName'])
                    pass
                else:
                    # timeout or non-take action, set to stand
                    logger.info('stand action or timeout received from ' + str(players[roundPlayerIdx]['userId']) + ' ' + players[roundPlayerIdx]['userName'])
                    pass
            for task in unfinished:
                task.cancel()

        output = "< Host's turn >"
        await ctx.channel.send(output)
        round += 1
    
    msg = "Game End"
    await ctx.channel.send(msg)

