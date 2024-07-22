from typing import Any, Iterable
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
from scrapy.http import Response
import json

class OnTheMarket(scrapy.Spider):

    name = 'onTheMarket'
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    }

    def start_requests(self) -> Iterable[scrapy.Request]:
        url = 'https://www.onthemarket.com/for-sale/property/abbey-gate/'
        yield scrapy.Request(url=url, headers=self.headers, callback=self.parse)

    def parse(self, response: Response, **kwargs: Any) -> Any:
        html = ''
        # self.log(response.status)

        with open('template.html', 'r', encoding='utf-8') as html_file:
            # html_file.write(response.text)
            for line in html_file.read():
                html += line

        response = Selector(text=html) 

        for card in response.css('li.otm-PropertyCard'):
            items = {
                "title" : card.css('span.title').css('a').css('span::text').get(),
                "address" : card.css('span.address').css('a::text').get(),
                "description": [ item.css("li::text").get() for item in card.css('li.otm-ListItemOtmBullet') ],
                "price": card.css('div.otm-Price').css('div.price::text').get().encode('ascii', 'ignore').decode('utf-8').strip(),
                "contact": card.css('div.otm-Telephone::text').get()
            }

            print(json.dumps(items, indent=2))
        # print(response.css('li.otm-PropertyCard'))
        # print(response.xpath('//li[@class="otm-PropertyCard"]/text()'))


if __name__ == '__main__':
    process = OnTheMarket()
    process.parse("")

    # process = CrawlerProcess()
    # process.crawl(OnTheMarket)
    # process.start()