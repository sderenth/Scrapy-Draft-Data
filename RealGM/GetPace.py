import scrapy
import psycopg2
from bs4 import BeautifulSoup
 
try:
    conn = psycopg2.connect(database='my_database', user='user_name', password='password', host='localhost')
    print("Connected Foo!!")
except:
    print("I am unable to connect to the database.")
       
cur = conn.cursor()
 
base_urls = []
year = 2003
while (year < 2013):
    seasonUrl = 'http://basketball.realgm.com/ncaa/team-stats/' + str(year) + '/Advanced_Stats/Team_Totals/0'
    base_urls.append(seasonUrl)
    year = year + 1
   
class RealGMSpider(scrapy.Spider):
    name = "RealGMTeamPace"
    start_urls = base_urls
          
    def parse(self, response):
        season = response._url.split('/')[-4]
        
        cur.execute("""SELECT DISTINCT team, season FROM prenbastats2003to2012 WHERE season = """ + season + """;""")
        teams = cur.fetchall()
           
        soup = BeautifulSoup(response.text, "lxml")
         
        complete_team_pace = []
        for team in teams:
            team_name = soup.find_all('a', text=team[0])[0]
            pace = team_name.parent.parent.find_all('td')[-1]
            team_plus_pace = team + (pace.getText(),)
            complete_team_pace.append(team_plus_pace)
             
        for team in complete_team_pace: 
            cur.execute("""INSERT INTO team_pace_for_prenbastats2003to2012 
                            VALUES (%s, %s, %s)""", team)
            conn.commit()
