import scrapy
 
class BballRefBPMSpider(scrapy.Spider):
    name = "bpmfrom94"
    start_urls = ['http://www.basketball-reference.com/leagues/NBA_1995_advanced.html']
             
    def parse(self, response):
        for row in response.xpath('//table[@id="advanced_stats"]/tbody/tr'):
            if row.xpath('./@class').extract_first() == 'full_table':
                yield {
                    'id' : row.xpath('.//th/@csk').extract_first(),
                    'playerName' : row.xpath('./td[1]/@csk').extract_first(),
                    'playerId' : row.xpath('./td[1]/@data-append-csv').extract_first(),
                    'season' : int(response.xpath('//title/text()').extract()[0].split('-')[0]) + 1,
                    'age' : row.xpath('./td[3]/text()').extract_first(),
                    'BPM' : row.xpath('./td[27]/text()').extract_first()
                    
                }       
                
        next_page = response.xpath('//a[@class="button2 next"]/@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)