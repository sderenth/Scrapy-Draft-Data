# Scrapy-Draft-Data
Scrapy spiders for crawling basketball websites ([Basketball-Reference](http://www.basketball-reference.com/) and [RealGM](http://basketball.realgm.com/)) and depositing statistics relevant to the NBA Draft in a PostgreSQL database.

[Scrapy](https://doc.scrapy.org/en/1.2/index.html) is a python webcrawling framework.

Each file, excluding BasicModelDataPrep.py and ExtraByHandPlayerStatCompilings.py, is a spider, or webcrawling bot, that can only function inside of scrapy project with the appropriate auxiliary files. In case you adapt these for your own use, know that I did not alter any of the default configurations, settings, piplines, or items files. 

*Attention:* Basketball-Reference [discourages](http://www.sports-reference.com/data_use.html) scraping large datasets from their site. I only became aware of this policy after having written several Basketball-Reference spiders. For the sake of understanding, I have included two Basketball-Reference spiders in this repository, however most are directed at RealGM. 
