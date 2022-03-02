from ast import Index
from urllib import request
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from scrapy.http import XmlResponse
from driver.config import selDriver
import pandas as pd
from selenium.common.exceptions import NoSuchElementException

import requests
import time



class Scrapper: 
    def __init__(self, modo):
        self.driver = selDriver().driver
        self.modo = modo
        self.driver.get(f'https://www.netimoveis.com/{self.modo}/bahia/salvador?transacao=venda&localizacao=BR-BA-salvador---&pagina=1')
        
    def get_page_content(self):

        time.sleep(0.5)
        self.click_next()
        time.sleep(0.5)
        self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        imoveis_container = self.soup.find('div', {'class', 'row imoveis'})
        imoveis           = imoveis_container.find_all('article', {'class': 'card-imovel'})
        imoveis_list = list()

        for imovel in imoveis:
        
            title            = imovel.find('div', {'class': 'mb-2 tipo'}).text
            endereco         = imovel.find('div', {'class': 'endereco'}).text
            metros_quadrados = imovel.find('div', {'class': 'caracteristica area'}).text # Vê se n tem uma forma de pegar só o número já aqui
            quartos          = imovel.find('div', {'class': 'caracteristica quartos'}).text # Vê se n tem uma forma de pegar só o número já aqui
            vagas            = imovel.find('div', {'class': 'caracteristica vagas'}).text # Vê se n tem uma forma de pegar só o número já aqui
            banheiros        = imovel.find('div', {'class': 'caracteristica banheiros'}).text # Vê se n tem uma forma de pegar só o número já aqui
            valores          = imovel.find('div', {'class': 'valor'}).text


            tipo = title.split('\n')[2]

            tipo =  ''.join([l.replace(' ', '') for l in tipo])
            if 'quarto' in tipo:
                tipo = tipo[:-7]
    

            metros_quadrados = ''.join([l.replace(' ', '') for l in metros_quadrados.split(' ')])
            metros_quadrados = float(metros_quadrados.split('\n')[-2].replace('m²', '').replace('.','').replace(',', '.'))
            
            def clean_spaces(var, to_replace): 
                var = ''.join([l.replace(' ', '').replace('-', '0') for l in var.split(' ')])
                var = int(var.split('\n')[-2].replace(to_replace + 's', '').replace(to_replace, ''))
                return var
            
            
            quartos = clean_spaces(quartos, 'quarto')
            vagas = clean_spaces(vagas, 'vaga')
            banheiros = clean_spaces(banheiros, 'banheiro')

            valores = ''.join([l.replace(' ', '') for l in valores.split(' ')])
            valores = int(valores.split('\n')[1].replace('R$', '')[1:].replace('.', ''))

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
                numero = endereco.split(',')[2]
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

            print(imovel_dict)
            
            imoveis_list.append(imovel_dict)

        return imoveis_list

    def get_page_number(self):

        self.driver.get(f'https://www.netimoveis.com/{self.modo}/bahia/salvador?transacao=venda&localizacao=BR-BA-salvador---&pagina=1')
        
        numero_paginas = self.driver.find_element_by_xpath('/html/body/main/article/section/div/div/section[2]/nav/ul/li[9]/a').text
        return int(numero_paginas)
    
    def click_next(self):

        prox_btn = self.driver.find_element_by_partial_link_text('Próximo')
        prox_btn.click()





scrapper = Scrapper('venda')
imoveis_geral = list()


numero_paginas = scrapper.get_page_number()
print(numero_paginas)

for i in range(numero_paginas):
    try:
        imoveis_list = scrapper.get_page_content()
        imoveis_geral = imoveis_geral + imoveis_list
    except NoSuchElementException:
        pass


df = pd.DataFrame(imoveis_geral)
print(df.head())
df.to_csv('venda_salvador.csv')