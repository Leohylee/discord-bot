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
    if util.getProperty(ctx, 'game_exists'):
        await ctx.channel.send(config.BJ_MSG['GAME_EXISTS_WAIT_FOR_NEXT_ROUND'])
    else:
        util.setProperty(ctx, 'game_exists', True)
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

    host = { 'deck': player_deck, 'stand': False, 'points': 0 }

    players = []
    for userId, userName in players_data:
        player_deck = ''
        drawCard, deck = util.drawCard(deck)
        player_deck += drawCard
        drawCard, deck = util.drawCard(deck)
        player_deck += drawCard
        players.append( { 'userId': userId, 'userName': userName, 'deck': player_deck, 'stand': False, 'points': 0 } )
    
    # players.append( { 'userId': 'testID', 'userName': 'testName', 'deck': 'XX', 'stand': True } )

    logger.info(players)

    while round <= 5:
        for roundPlayerIdx in range(len(players)):
            logger.info(f"Round {str(round)} / Player's turn: {str(players)}")
            if players[roundPlayerIdx]['stand'] or min(util.calcPoints(ctx, players[roundPlayerIdx]['deck'])) >= util.getProperty(ctx, 'BJ_WINNING_POINT'):
                continue
            
            output = util.showRoundInfo(ctx, round, host, players)
            output += f"<@{players[roundPlayerIdx]['userId']}> It's your turn. (t: take, s: stand)"

            ctx.bot.turn_lock = players[roundPlayerIdx]['userId']
            logger.info(f'Round {str(round)} / Player {str(players)} / Round lock delegated')
            await ctx.channel.send(output)

            count_timer = asyncio.sleep(util.getProperty(ctx, 'BJ_ROUND_PLAYER_INPUT_WAIT_TIME_SECOND'))
            stop_future = asyncio.Future()
            ctx.bot.stopTimer = stop_future

            finished, unfinished = await asyncio.wait([count_timer, stop_future], return_when=FIRST_COMPLETED)
            ctx.bot.turn_lock = None
            logger.info('round lock has reset')

            for x in finished:
                roundAction = x.result()
                logger.info(f'Round {str(round)} / Player {str(players)} / Round action: {str(roundAction)}')
                if roundAction == 'take':
                    logger.info(f'Round {str(round)} / Player {str(players)} / take action received')
                    drawCard, deck = util.drawCard(deck)
                    players[roundPlayerIdx]['deck'] += drawCard
                    calculated_points = util.calcPoints(ctx, players[roundPlayerIdx]['deck'])
                    filtered_points = list(filter(lambda point: point <= util.getProperty(ctx, 'BJ_WINNING_POINT'), calculated_points))
                    if len(filtered_points) > 0:
                        players[roundPlayerIdx]['points'] = max(filtered_points)
                    else:
                        players[roundPlayerIdx]['points'] = max(calculated_points)
                        players[roundPlayerIdx]['stand'] = True
                    
                    if players[roundPlayerIdx]['points'] == util.getProperty(ctx, 'BJ_WINNING_POINT'):
                        players[roundPlayerIdx]['stand'] = True
                else:
                    # timeout or non-take action, set to stand
                    logger.info(f'Round {str(round)} / Player {str(players)} / stand action or timeout received')
                    players[roundPlayerIdx]['points'] = max(util.calcPoints(ctx, players[roundPlayerIdx]['deck']))
                    players[roundPlayerIdx]['stand'] = True
            for task in unfinished:
                task.cancel()

        output = util.showRoundInfo(ctx, round, host, players)
        output += "< Host's turn >"
        await ctx.channel.send(output)
        round += 1
    
    await ctx.channel.send(config.BJ_MSG['GAME_END_HEADLINE'])

    util.setProperty(ctx, 'game_exists', False)
