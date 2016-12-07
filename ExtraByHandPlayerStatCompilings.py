import psycopg2
from operator import itemgetter

try:
    conn = psycopg2.connect(database='my_database', user='user_name', password='password', host='localhost')
    print("Connected Foos!!")
except:
    print("I am unable to connect to the database.")
    
cur = conn.cursor()

by_hand_players = [['Derrick-Williams6644', 'willide02', 'skip me'], ['Jeff-Ayres1636', 'pendeje02', 'skip me'],
                   ['JJ-Barea298', 'bareajo01', 'skip me'], ['Kemba-Walker2181', 'walkeke02', 'skip me'],
                   ['Tobias-Harris7119', 'harrito02', 'skip me'], ['Mario-West364', 'westma02', 'skip me'],
                   ['Kevin-Martin392', 'martike02', 'skip me'],
                   ['Brandan-Wright45', 'wrighbr03', 'skip me'], ['Marcus-D-Williams77', 'willima03', 'skip me'],
                   ['Anthony-Davis13305', 'davisan02', 'skip me'], ['Brandon-Knight2258', 'knighbr03', 'skip me'],
                   ['Jason-Smith51', 'smithja02', 'skip me'], ['James-Johnson1604', 'johnsja01', 'skip me'],
                   ['Reggie-Williams1783', 'willire02', 'skip me'], ['Henry-Walker814', 'walkebi01', 'skip me'],
                   ['Dahntay-Jones445', 'jonesda02', 'skip me'], ['Al-Farouq-Aminu2180', 'aminual01', 'skip me'],
                   ['Chris-Johnson9587', 'johnsch04', 'skip me'], ['Tristan-Thompson7103', 'thomptr01', 'skip me'],
                   ['Deron-Williams60', 'willide01', 'skip me'], ['Shelden-Williams68', 'willish02', 'skip me'],
                   ['Shawne-Williams90', 'willish03', 'skip me'], ['Markieff-Morris4191', 'morrima02', 'skip me'],
                   ['Jordan-Crawford4441', 'crawfjo02', 'skip me'], ['Marvin-Williams59', 'willima02', 'skip me'],
                   ['Paul-Millsap112', 'millspa01', 'skip me'], ['Patty-Mills1632', 'millspa02', 'skip me'],
                   ['Marcus-Morris4078', 'morrima03', 'skip me']]

for player in by_hand_players:
    player.remove('skip me')

for player in by_hand_players:
    realGM_playerid_tuple = (player[0],)
    cur.execute("""SELECT AVG(age) AS "AGE", 
                        AVG("GS")/AVG("GP") AS "% GS", 
                        AVG("MIN")/AVG("GP") AS "MIN/G", 
                        AVG("FGA")/AVG("MIN") AS "FGA/MIN",
                        AVG("FG%") AS "FG%", 
                        AVG("3PA")/AVG("MIN") AS "3PA/MIN", 
                        AVG("3P%") AS "3P%", 
                        AVG("FTA")/AVG("MIN") AS "FTA/MIN", 
                        AVG("FT%") AS "FT%", 
                        AVG("ORB")/AVG("MIN") AS "ORB/MIN", 
                        AVG("DRB")/AVG("MIN") AS "DRB/MIN", 
                        AVG("TRB")/AVG("MIN") AS "TRB/MIN", 
                        AVG("AST")/AVG("MIN") AS "AST/MIN", 
                        AVG("STL")/AVG("MIN") AS "STL/MIN", 
                        AVG("BLK")/AVG("MIN") AS "BLK/MIN", 
                        AVG("PF")/AVG("MIN") AS "PF/MIN", 
                        AVG("TOV")/AVG("MIN") AS "TOV/MIN", 
                        AVG("PTS")/AVG("MIN") AS "PTS/MIN", 
                        AVG("TS%") AS "TS%", 
                        AVG("ORB%") AS "ORB%", 
                        AVG("DRB%") AS "DRB%", 
                        AVG("TRB%") AS "TRB%", 
                        AVG("AST%") AS "AST%", 
                        AVG("TOV%") AS "TOV%", 
                        AVG("STL%") AS "STL%", 
                        AVG("BLK%") AS "BLK%",
                        AVG("USG%") AS "USG%", 
                        AVG("PPR") AS "PPR", 
                        AVG("ORtg") AS "ORtg", 
                        AVG("DRtg") AS "DRtg", 
                        AVG("PER") AS "PER"  
                FROM prenbastats2003to2012
                WHERE playerid = '""" + realGM_playerid_tuple[0] + """';""")
    player_avg_stats = cur.fetchall()
    player_avg_stats = list(player_avg_stats[0])
    for stat in player_avg_stats:
        player.append(stat)
        
for player in by_hand_players:
    cur.execute("SELECT age, bpm FROM playerbpmseasons WHERE playerid = '" + player[1] + "';")
    ages_bpms = cur.fetchall()
    sortedBpm = []
    for i in range(len(ages_bpms)):
        sortedBpm.append(sorted(ages_bpms, key=itemgetter(1))[i][1])
    if len(sortedBpm) >= 4:
        mean = (sortedBpm[2] + sortedBpm[3])/2
        player.append(mean)
 
for player in by_hand_players:
    player.remove(player[1])
    player_tuple = tuple(player)
    cur.execute("""INSERT INTO avg_pre_nba_stats_2003to2012 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                   %s, %s, %s, %s, %s, %s, %s, %s);""", player_tuple)
    conn.commit()
