import scrapy
import psycopg2
from bs4 import BeautifulSoup
import re
  
try:
    conn = psycopg2.connect(database='my_database', user='user_name', password='password', host='localhost')
    print("Connected Foos!!")
except:
    print("I am unable to connect to the database.")
   
cur = conn.cursor()
  
base_urls = []
year = 2003
while (year < 2013):
    draftUrl = 'http://basketball.realgm.com/nba/draft/past_drafts/' + str(year)
    base_urls.append(draftUrl)
    year = year + 1
  
class RealGMSpider(scrapy.Spider):
    name = "RealGMPlayerStats"
    start_urls = base_urls
         
    def parse(self, response):
        soup = BeautifulSoup(response.text, "lxml")

        href_wild = re.compile('./Summary')
        player_partial_hrefs = soup.find_all('a', href=href_wild)
        
        for i in range(len(player_partial_hrefs)):
            player_page = 'http://basketball.realgm.com' + player_partial_hrefs[i]['href']
            if player_page is not None:
                yield scrapy.Request(player_page, callback=self.parse_player_page)
        
    def parse_player_page(self, response):
        
        def getNCAAdata(soup):
            total_h2tag = soup.find_all('h2', text='NCAA Season Stats - Totals')[0]
            total_data_rows = total_h2tag.next_sibling.find_all('tr')[1:-1]
            
            boxscore_player_data = []
            for i in range(len(total_data_rows)):
                if total_data_rows[i].find_all('td')[3].getText() != '-':
                    season = []
                    for td in total_data_rows[i].find_all('td'):
                        season.append(td.getText())
                    boxscore_player_data.append(season)
            for season in boxscore_player_data:
                season[0] = int(season[0].split('-')[0]) + 1
            
            advanced_h2tag = soup.find_all('h2', text='NCAA Season Stats - Advanced Stats')[0]
            advanced_data_rows = advanced_h2tag.next_sibling.find_all('tr')[1:-1]
            
            advanced_player_data = []
            for i in range(len(advanced_data_rows)):
                if advanced_data_rows[i].find_all('td')[3].getText() != '-':
                    season = []
                    for td in advanced_data_rows[i].find_all('td'):
                        season.append(td.getText())
                    advanced_player_data.append(season)
            
            name_list = soup.find_all('a', class_='selected')[0]['href'].split('/')
            playerid = name_list[2]+name_list[4]
            
            year_drafted = int(soup.find_all('a', href=re.compile("/nba/draft/past_drafts/"))[0].getText().split(' ')[0])
            birthday = soup.find_all('a', href=re.compile("/info/birthdays/"))[0]['href'].split('/')[3]
            birthday_lst = [int(birthday[0:4]), int(birthday[4:6]), int(birthday[6:8])]
            days_in_months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            days_old = birthday_lst[2]
            for i in range(birthday_lst[1]-1):
                days_old = days_old + days_in_months[i]
            age_jan1_year_drafted = (365*(year_drafted - birthday_lst[0])) + days_old
                
            pick = soup.find_all('strong', text="Drafted:")[0].parent.getText()
            if pick == 'Drafted: Undrafted':
                pick = 61
            elif pick.split(' ')[2][0] == '1':
                pick = int(pick.split(' ')[4][:-1])
            elif pick.split(' ')[2][0] == '2':
                pick = int(pick.split(' ')[4][:-1]) + 30
            
            all_player_data = boxscore_player_data
            for i in range(len(all_player_data)):
                all_player_data[i].insert(0, playerid)    
                all_player_data[i].insert(1, year_drafted)
                all_player_data[i].insert(2, pick)
                all_player_data[i].insert(3, age_jan1_year_drafted)
                for j in range(5, 21):
                    all_player_data[i].append(advanced_player_data[i][j])
            
            return all_player_data
        
        def getInternationalData(soup):
            inter_total_h2tag = soup.find_all('h2', text='International Regular Season Stats - Totals')[0]
            inter_total_data_rows = inter_total_h2tag.next_sibling.find_all('tr')[1:]
            
            boxscore_player_data = []
            for i in range(len(inter_total_data_rows)):
                if inter_total_data_rows[i].find_all('td')[1].getText() != 'All Teams':
                    season = []
                    for td in inter_total_data_rows[i].find_all('td'):
                        season.append(td.getText())
                    boxscore_player_data.append(season)
            for season in boxscore_player_data:
                season[0] = int(season[0].split('-')[0]) + 1
            
            inter_advanced_h2tag = soup.find_all('h2', text='International Regular Season Stats - Advanced Stats')[0]
            inter_advanced_data_rows = inter_advanced_h2tag.next_sibling.find_all('tr')[1:]
             
            advanced_player_data = []
            for i in range(len(inter_advanced_data_rows)):
                if inter_total_data_rows[i].find_all('td')[1].getText() != 'All Teams':
                    season = []
                    for td in inter_advanced_data_rows[i].find_all('td'):
                        season.append(td.getText())
                    advanced_player_data.append(season)
             
            name_list = soup.find_all('a', class_='selected')[0]['href'].split('/')
            playerid = name_list[2]+name_list[4]
            
            year_drafted = int(soup.find_all('a', href=re.compile("/nba/draft/past_drafts/"))[0].getText().split(' ')[0])
            birthday = soup.find_all('a', href=re.compile("/info/birthdays/"))[0]['href'].split('/')[3]
            birthday_lst = [int(birthday[0:4]), int(birthday[4:6]), int(birthday[6:8])]
            days_in_months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            days_old = birthday_lst[2]
            for i in range(birthday_lst[1]-1):
                days_old = days_old + days_in_months[i]
            age_jan1_year_drafted = (365*(year_drafted - birthday_lst[0])) + days_old
                
            pick = soup.find_all('strong', text="Drafted:")[0].parent.getText()
            if pick == 'Drafted: Undrafted':
                pick = 61
            elif pick.split(' ')[2][0] == '1':
                pick = int(pick.split(' ')[4][:-1])
            elif pick.split(' ')[2][0] == '2':
                pick = int(pick.split(' ')[4][:-1]) + 30
            
            all_player_data = boxscore_player_data
            for i in range(len(all_player_data)):
                all_player_data[i].insert(0, playerid)    
                all_player_data[i].insert(1, year_drafted)
                all_player_data[i].insert(2, pick)
                all_player_data[i].insert(3, age_jan1_year_drafted)
                for j in range(5, 21):
                    all_player_data[i].append(advanced_player_data[i][j])
            
            return all_player_data
        
        def checkGetSendData(soup):
            span = soup.find_all('span', class_='nowrap')
            years_of_service = int(soup.find_all('div', class_='profile-wrap')[0].find_all('p')[1].getText().split(' ')[0])
            if years_of_service >= 4:
                if span[1].a['href'] == '#NCAA':
                    for season in getNCAAdata(soup):
                        if season[1] >= season[4]:
                            tupleSeason = tuple(season)
                            cur.execute("""INSERT INTO prenbastats2003to2012 
                                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                                                tupleSeason)
                            conn.commit()
                elif span[1].a['href'] == '#International':
                    for season in getInternationalData(soup):
                        if season[1] >= season[4]:
                            tupleSeason = tuple(season)
                            cur.execute("""INSERT INTO prenbastats2003to2012 
                                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                                                tupleSeason)
                            conn.commit()   
        
        
        beaut_soup = BeautifulSoup(response.text, "lxml")
        checkGetSendData(beaut_soup)
