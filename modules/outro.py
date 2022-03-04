from ast import Index
from urllib import request
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from scrapy.http import XmlResponse
from driver.config import selDriver
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import requests
import time



class Scrapper: 
    def __init__(self):
        self.driver = selDriver().driver
        self.driver.get('https://www.cesarrego.com.br/busca/aluguel/apartamento/fortaleza/')
        
    def get_page_content(self):

        wait = WebDriverWait(self.driver, 30)
        content = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "descricao")))
        time.sleep(2)

        self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        imoveis_container = self.soup.find('div', {'class', 'body-content'})
        enderecos = imoveis_container.find_all('div', {'class': 'cardImovel'})
        for endereco in enderecos:
            title = endereco.find('div', {'class', 'valor'}).text
            print(title)

        

        # title = endereco.find('h2', {'class':'descricao'}).text

        # for imovel in imoveis:
        
        #     endereco            = imovel.find('div', {'class': 'search-info'}).text

             
        #     imovel_dict = dict()

        #     imovel_dict['endereco']             = endereco
            
        # print(title)
            
        #     imoveis_list.append(imovel_dict)

        # return imoveis_list

    # def get_page_number(self):
    #     number = self.driver.find_element_by_xpath('/html/body/main/article/section/div/div/section[2]/nav/ul/li[9]/a').text
    #     return int(number)

    # def click_next(self):

    #     wait = WebDriverWait(self.driver, 30)
    #     content = wait.until(
    #     EC.presence_of_element_located((By.CLASS_NAME, "endereco")))
    #     time.sleep(2)
    #     element = self.driver.find_element_by_partial_link_text('Próximo')

    #     element.click()
        
scrapper = Scrapper()
imoveis_geral = list()
scrapper.get_page_content()


# number = scrapper.get_page_number()
# print(number)

# for i in range(number):
#     try:
#         imoveis_list = scrapper.get_page_content()
#         imoveis_geral = imoveis_geral + imoveis_list
#     except NoSuchElementException:
#         pass


# df = pd.DataFrame(imoveis_geral)
# print(df.head())

# df.to_csv('aluguel_salvador.csv')