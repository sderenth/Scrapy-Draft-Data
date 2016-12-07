import psycopg2
from operator import itemgetter

try:
    conn = psycopg2.connect(database='my_database', user='user_name', password='password', host='localhost')
    print("Connected Foos!!")
except:
    print("I am unable to connect to the database.")
    
cur = conn.cursor()

cur.execute("""SELECT DISTINCT playerid FROM prenbastats2003to2012;""")
playerid_tuple = cur.fetchall()
realGM_playerids = [list(player_tuple) for player_tuple in playerid_tuple]

for player in realGM_playerids:
    player_name = player[0].split('-', 1)
    last_name = ''.join(i for i in player_name[1] if not i.isdigit())
    last_name = last_name.replace('-', '')
    if len(last_name) > 4:
        player.insert(1, ((last_name[:5] + player_name[0][:2] + '%').lower()))
    else:
        player.insert(1, ((last_name + player_name[0][:2] + '%').lower()))
both_playerids = realGM_playerids

playerid_problems = []
for i in range(len(both_playerids)):
    cur.execute("SELECT DISTINCT playerid FROM playerbpmseasons WHERE playerid LIKE '" + both_playerids[i][1] + "';")
    playerid_select = cur.fetchall()
    if len(playerid_select) != 1:
        playerid_problems.append(both_playerids[i][1])

for i in range(len(both_playerids)):
    if both_playerids[i][1] in playerid_problems: 
        both_playerids[i].append('skip me')

for player in both_playerids:
    if len(player) < 3:
        cur.execute("SELECT age, bpm FROM playerbpmseasons WHERE playerid LIKE '" + player[1] + "';")
        ages_bpms = cur.fetchall()
        sortedBpm = []
        for i in range(len(ages_bpms)):
            sortedBpm.append(sorted(ages_bpms, key=itemgetter(1))[i][1])
        if len(sortedBpm) >= 4:
            mean = (sortedBpm[2] + sortedBpm[3])/2
            player.append(mean)

problems = []
by_hand = []
for player in both_playerids:
    if len(player) > 2:
        if type(player[2]) == type(3.4):
            player_tuple = (player[2], player[0])
            cur.execute("""UPDATE avg_pre_nba_stats_2003to2012 SET "BPM (avgOfYears3&4)" = %s WHERE playerid = %s;""", player_tuple)
            conn.commit() 
        elif player[2] == 'skip me':
            by_hand.append(player)
        else:
            problems.append(player)
    else:
        problems.append(player)
        player_tuple = (player[0],)
        cur.execute("DELETE FROM avg_pre_nba_stats_2003to2012 WHERE playerid = '" + player_tuple[0] + "';")
        conn.commit()
        
print(problems)
print(by_hand)
        
