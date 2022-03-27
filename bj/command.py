from . import util

def rank(conn):
    data = util.getRankData(conn)
    output = '🏆🏆🏆 leaderboard (credit) 🏆🏆🏆\n'
    for row in data:
        balance = '${:0,.0f}'.format(float(row[2])).replace('$-','-$')
        output += (f'{row[1]}:\t{balance}\n')
    return output
