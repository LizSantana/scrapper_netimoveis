import scrapy
from scrapy_scrapingbee import ScrapingBeeSpider, ScrapingBeeRequest

class NetimoveisSpider(ScrapingBeeSpider):
    name = 'imob'
    # name = 'netimoveis'
    # allowed_domains = ['netimoveis.com']

    def start_requests(self):
        
        url = 'https://www.megaimoveis.com/imoveis/para-alugar/fortaleza'
        yield ScrapingBeeRequest(url=url, callback=self.parse)

    def parse(self, response):
        
        elements = response.css('div.card-listing')

        for element in elements:
            price = element.css('span.location *::text').getall()[-1]
            price =  float(price.replace(' ', '').replace('R$', '').replace('.', '').replace(',', '.').replace('Sob Consulta', '0'))
            print(price)
            # yield {
            #     'title': element.css('h3.card-text *::text').getall(),
            #     'bairro': element.css('h2.card-title *::text').getall(),
            #     'metros': element.css('span.h-money *::text').getall(),
            #     'banheiros': element.css()
            # }
        
        # next_button = response.css('//*[@id="listings-intwyt"]/div/div[2]/div[3]/div[2]/div[2]/div/div[3]/a/@href').get()

        # print(next_button)

        # if next_button is not None:
        #     yield ScrapingBeeRequest(url=response.urljoin(next_button), callback={self.parse})
