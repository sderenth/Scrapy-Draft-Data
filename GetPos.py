import scrapy
import psycopg2
from bs4 import BeautifulSoup
from _ast import Num
  
try:
    conn = psycopg2.connect(database='basketball', user='Sean', password='anders', host='localhost')
    print("Connected Foos!!")
except:
    print("I am unable to connect to the database.")
   
cur = conn.cursor()

cur.execute("""SELECT DISTINCT playerid FROM prenbastats2003to2012;""")
playerids = cur.fetchall()
player_urls = []
for playerid in playerids:
    name = ''
    for letter in playerid[0]:
        if not letter.isdigit():
            name+=letter
    num = ''
    for digit in playerid[0]:
        if digit.isdigit():
            num+=digit
    player_urls.append('http://basketball.realgm.com/player/' + name + '/Summary/' + num)


class RealGMSpider(scrapy.Spider):
    name = "RealGMPlayerPos"
    start_urls = player_urls
     
    def parse(self, response):
        playerId = response._url.split('/')[-3] + response._url.split('/')[-1]
        soup = BeautifulSoup(response.text, "lxml")
        pos = soup.find_all('h2')[0].contents[1].getText()
        cur.execute("""UPDATE prenbastats2003to2012 SET "Position" = '""" + pos + """' 
                        WHERE playerid = '""" + playerId + """';""")
        conn.commit()