import scrapy
import datetime
from ..items import ScrapejnmarketItem

class JnmarketSpider(scrapy.Spider):
    name = 'jnmarket'
    page_number = 1
    start_urls = [
        'http://www.jnmarket.net/import/list-2_1.html'
    ]
    
    def parse(self, response):
        mainElem = response.css('table.price-table tbody')
        for row in mainElem.css('tr'):
            item = ScrapejnmarketItem()
            item['name'] = row.css('td:nth-child(1)::text').extract()
            item['origin'] = row.css('td:nth-child(2)::text').extract()
            item['price'] = row.css('td:nth-child(3)::text').extract()
            item['specification'] = row.css('td:nth-child(4)::text').extract()
            item['date'] = datetime.datetime.strptime(row.css('td:nth-child(5)::text').get(), '%d-%m-%y').strftime(
                '%Y-%m-%d')
            yield item

            next_page = 'http://www.jnmarket.net/import/list-2_'+str(JnmarketSpider.page_number) +'.html'
            if JnmarketSpider.page_number <= 3:
                JnmarketSpider.page_number +=1
            yield response.follow(next_page, callback = self.parse)