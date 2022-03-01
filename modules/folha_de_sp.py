from urllib import request
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from scrapy.http import XmlResponse
from driver.config import selDriver

import requests


class Scrapper: 
    def __init__(self, modo):
        self.driver = selDriver().driver
        self.modo = modo
        #r = requests.get('https://www.netimoveis.com/venda/bahia/salvador/apartamento?tipo=apartamento&transacao=venda&localizacao=BR-BA-salvador---&pagina=1')
        #self.soup = BeautifulSoup(r.content, 'html.parser')
        self.soup = BeautifulSoup(driver.page_source, 'html.parser')

        #title = soup.find('h1', {'class': 'busca-titulo'}).text
        #print(title)
    def get_page_content(self):
        self.driver.get(f'https://www.netimoveis.com/{self.modo}/bahia/salvador?transacao=venda&localizacao=BR-BA-salvador---&pagina=1')

        imoveis_container = self.soup.find('div', {'class', 'row imoveis'})
        imoveis           = imoveis_container.find_all('div', {'class': 'col-12'})
        
        imoveis_list = list()

        for imovel in imoveis:
            
            title = soup.find



Scrapper().get_page_content()