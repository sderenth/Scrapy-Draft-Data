import scrapy
import psycopg2
from bs4 import BeautifulSoup
    
try:
    conn = psycopg2.connect(database='basketball', user='Sean', password='anders', host='localhost')
    print("Connected Foo!!")
except:
    print("I am unable to connect to the database.")
          
cur = conn.cursor()
   
base_urls = []
year = 2003
while (year < 2013):
    seasonUrl = 'http://www.sports-reference.com/cbb/seasons/' + str(year) + '-advanced-school-stats.html'
    base_urls.append(seasonUrl)
    year = year + 1
     
class BballDraftSpider(scrapy.Spider):
    name = "bballRefTeamSOSandSRS"
    start_urls = base_urls
            
    def parse(self, response):
        season = response._url.split('/')[-1][0:4]
 
        soup = BeautifulSoup(response.text, "lxml")
        data_rows = soup.tbody.find_all('tr')
        
        complete_team_ratings = []
        for tr in data_rows:
            if not tr.has_attr('class'):
                tds = tr.find_all('td')
                team = tds[0].getText()
                sos = tds[6].getText()
                srs = tds[5].getText()
                complete_team_ratings.append((team, season, sos, srs))
    
        for team in complete_team_ratings: 
            cur.execute("""INSERT INTO all_college_teams_sos_for_prenbastats2003to2012 
                            VALUES (%s, %s, %s, %s)""", team)
            conn.commit()