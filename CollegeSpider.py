import scrapy
import psycopg2
from operator import itemgetter
from bs4 import BeautifulSoup

try:
    conn = psycopg2.connect(database='my_database', user='user_name', password='password', host='localhost')
    print("Connected Foos!!")
except:
    print("I am unable to connect to the database.")
 
cur = conn.cursor()
 
#Get list of playerids.
cur.execute("""SELECT playerid FROM nbadraftfrom94 WHERE yeardrafted = 2001 AND playerid <> 'Null'""")
playersDrafted = cur.fetchall()
 
start_url_list = []
for player in playersDrafted:
        start_url_list.append('http://www.basketball-reference.com/players/' + player[0][0] + '/' + player[0] + '.html')
        
class DrafteeCollegeStatsSpider(scrapy.Spider):
    name = "DrafteeCollegeStats"
    start_urls = start_url_list
      
    def parse(self, response):
        comment = response.xpath('//div[@id="all_all_college_stats"]/comment()').extract_first()[10:-4]
        soup = BeautifulSoup(comment, 'lxml')
 
        data_rows = soup.tbody.find_all('tr')
        for tr in data_rows:
            tr.th.name = 'td'
  
        player_data = [[td.getText() for td in data_rows[i].findAll('td')[:19]]
                       for i in range(len(data_rows))]
 
        for i in range(len(player_data)):
            player_data[i][0] = int(player_data[i][0].split('-')[0]) + 1
            player_data[i].insert(0, response.xpath('//link[@rel="canonical"]/@href').extract_first().split('/')[5][:-5])
            for j in range(len(player_data[i])):
                if player_data[i][j] == '':
                    player_data[i][j] = None
         
        for seasons in player_data:
            tupleSeasons = tuple(seasons)
            cur.execute("""INSERT INTO collegebasicboxscorestats 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                            tupleSeasons)
            
        conn.commit()
