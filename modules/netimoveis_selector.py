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
    def __init__(self, modo):
        self.driver = selDriver().driver
        self.modo = modo
        self.driver.get(f'https://www.netimoveis.com/{self.modo}/bahia/salvador?transacao=venda&localizacao=BR-BA-salvador---&pagina=1')
        
    def get_page_content(self):

        wait = WebDriverWait(self.driver, 30)
        content = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "endereco")))
        time.sleep(2)
        time.sleep(0.8)
        self.click_next()
        time.sleep(0.8)
        #self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        imoveis = Selector(text=self.driver.page_source, type='html').css('article.card-imovel')
        imoveis_list = list()
        
        
            
        for i, imovel in enumerate(imoveis):
            
            ultimo = len(imoveis) - 1
            if ultimo == i:
                break
            #print(f'{ultimo = } {i = }')
            title            = imovel.css('h2 *::text').get()
            endereco         = imovel.css('div.endereco  *::text').get()
            metros_quadrados = imovel.css('div.caracteristica.area::text').extract()[1]
            quartos          = imovel.css('div.caracteristica.quartos::text').extract()[1]
            vagas            = imovel.css('div.caracteristica.vagas::text').extract()[1]
            banheiros        = imovel.css('div.caracteristica.banheiros::text').extract()[1]
            valores          = imovel.css('div.valor::text').get()

            tipo = title.split('\n')[1]
            tipo =  ''.join([l.replace(' ', '') for l in tipo])
            if 'quarto' in tipo:
             tipo = tipo[:-8]
    
            metros_quadrados = float(metros_quadrados.split(' ')[-2].replace('\n','').replace('.','').replace(',', '.'))
            
            def clean_spaces(var): 
                var = var.replace('-', '0').split('\n')[1].split(' ')[-1]
                return var
            
            
            quartos = clean_spaces(quartos)
            vagas = clean_spaces(vagas)
            banheiros = clean_spaces(banheiros)

            valores = ''.join([l.replace(' ', '') for l in valores.split(' ')])
            valores = float(valores.split('\n')[1].replace('R$', '')[1:].replace('.', ''))
            print(valores)

            bairro = None
            rua = None
            numero = None

            try: 
                bairro = endereco.split(',')[0]
            except IndexError: 
                pass
            try:
                rua = endereco.split(',')[1]
            except IndexError:
                pass
            try:
                numero = int(endereco.split(',')[2])
            except IndexError:
                pass
    
             
            imovel_dict = dict()

            imovel_dict['modo']             = self.modo
            imovel_dict['tipo']             = tipo
            imovel_dict['bairro']           = bairro
            imovel_dict['rua']              = rua
            imovel_dict['numero']           = numero
            imovel_dict['metros_quadrados'] = metros_quadrados
            imovel_dict['quartos']          = quartos
            imovel_dict['vagas']            = vagas
            imovel_dict['banheiros']        = banheiros
            imovel_dict['valor']            = valores

            print(imovel_dict)
            
            imoveis_list.append(imovel_dict)

        return imoveis_list

    def get_page_number(self):
        number = self.driver.find_element_by_xpath('/html/body/main/article/section/div/div/section[2]/nav/ul/li[9]/a').text
        return int(number)

    def click_next(self):

        wait = WebDriverWait(self.driver, 30)
        content = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "endereco")))
        time.sleep(2)
        element = self.driver.find_element_by_partial_link_text('Próximo')

        element.click()
        
scrapper = Scrapper('aluguel')
scrapper.get_page_content()
imoveis_geral = list()

number = scrapper.get_page_number()
print(number)

for i in range(number):
    try:
        imoveis_list = scrapper.get_page_content()
        imoveis_geral = imoveis_geral + imoveis_list
    except NoSuchElementException:
        pass


df = pd.DataFrame(imoveis_geral)
print(df.head())

# aluguel
df['tipo'] = df['tipo'].replace({
    "Apartament": "Apartamento",
    "Apartamento2": "Apartamento",
    "Apartamento3": "Apartamento", 
    "Apartamento4": "Apartamento", 
    "CasaComercial":"Casa Comercial", 
    "Casaemcondomínio": "Casa em condomínio", 
    "Conjuntodesalas": "Conjunto de salas",
    "Pontocomercial": "Ponto comercial" })

# venda
# df['tipo'] = df['tipo'].replace({
#     "Apartament": "Apartamento", 
#     "CasaComercial":"Casa Comercial", 
#     "Casaemcondomínio": "Casa em condomínio", 
#     "Conjuntodesalas": "Conjunto de salas",
#     "Pontocomercial": "Ponto comercial", 
#     "Terrenoemcondomínio": "Terreno em condomínio"
#     })


df.to_csv('aluguel_selector_salvador.csv')