import scrapy
import psycopg2
from bs4 import BeautifulSoup
 
try:
    conn = psycopg2.connect(database='basketball', user='Sean', password='anders', host='localhost')
    print("Connected Foo!!")
except:
    print("I am unable to connect to the database.")
        
cur = conn.cursor()
 
cur.execute("""SELECT playerid, season FROM prenbastats2003to2012 ORDER BY playerid, season;""")
player_seasons = cur.fetchall()
 
player_season_urls = []
for player_season in player_seasons:
    name = ''.join([i for i in player_season[0] if not i.isdigit()])
    num = ''.join([i for i in player_season[0] if i.isdigit()])
    url = 'http://basketball.realgm.com/player/' + name + '/GameLogs/' + num + '/NCAA/' + str(player_season[1])
    player_season_urls.append(url)
 
class RealGMSpider(scrapy.Spider):
    name = "RealGMGameLogs"
    start_urls = player_season_urls
           
    def parse(self, response):
        soup = BeautifulSoup(response.text, "lxml")
        data_rows = soup.tbody.find_all('tr')
        game_data = [[td.getText() for td in data_rows[i].findAll('td')]
                       for i in range(len(data_rows))]
        
        season = int(response._url.split('/')[-1])
        for game in game_data:
            game.insert(0, season)
        
        table_name = response._url.split('/')[-5] + response._url.split('/')[-3]

        cur.execute("SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name = '" + table_name + "');")  
        if cur.fetchone()[0] == False:    
            cur.execute("""CREATE TABLE \"""" + table_name + """\" (
                                    "Season" int,
                                    "Date" text,
                                    "Team" text,
                                    "Opponent" text,
                                    "W/L" text,
                                    "Status" text,
                                    "Pos" text,
                                    "MIN" text,
                                    "FGM" int,
                                    "FGA" int,
                                    "FG%" float,
                                    "3PM" int,
                                    "3PA" int,
                                    "3P%" float,
                                    "FTM" int,
                                    "FTA" int,
                                    "FT%" float,
                                    "ORB" int,
                                    "DRB" int,
                                    "REB" int,
                                    "AST" int,
                                    "STL" int,
                                    "BLK" int,
                                    "PTS" int,
                                    "FIC" float,
                                    "PF" int,
                                    "TOV" int,
                                    id serial PRIMARY key);""")
          
            for game in game_data:
                gameTuple = tuple(game)
                cur.execute("""INSERT INTO \"""" + table_name + """\" VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                               %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", gameTuple)
            conn.commit()
               
        else:
            for game in game_data:
                gameTuple = tuple(game)
                cur.execute("""INSERT INTO \"""" + table_name + """\" VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                               %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", gameTuple)
            conn.commit()


        