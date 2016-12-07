# Scrapy-Draft-Data
Scrapy spiders for crawling basketball websites ([Basketball-Reference](http://www.basketball-reference.com/) and [RealGM](http://basketball.realgm.com/)) and depositing statistics relevant to the NBA Draft in a PostgreSQL database.

[Scrapy](https://doc.scrapy.org/en/1.2/index.html) is a python webcrawling framework.

Each file, excluding BasicModelDataPrep.py and ExtraByHandPlayerStatCompilings.py, is a spider, or webcrawling bot, that can only function inside of scrapy project with the appropriate auxiliary files. In case you adapt these for your own use, know that I did not alter any of the default configurations, settings, piplines, or items files. 

*Attention:* Basketball-Reference does not give permission to scrape large amounts of their statistics. While the majority of the spiders here are written for RealGM, I included several for Basketball-Reference that were created before I became aware of thier policy. 
