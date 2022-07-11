import scrapy
from scrapy.http import XmlResponse
from driver.config import selDriver
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import requests
import time

import scrapy


class MySpider(scrapy.Spider):
    name = 'netimoveis_spider'
    allowed_domains = ['netimoveis.com']

    def __init__(self):
        self.driver = selDriver().driver

    def start_requests(self):
        url = 'https://www.netimoveis.com/aluguel/bahia/salvador?transacao=aluguel&localizacao=BR-BA-salvador---&pagina=1'
        yield scrapy.Request(url=url, callback= self.parse)


    def parse(self, response):
        self.driver.get(response.url)

        wait = WebDriverWait(self.driver, 30)
        content = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "endereco")))
        time.sleep(2)
        time.sleep(0.8)
        self.click_next()
        time.sleep(0.8)

        elemento = response.xpath('/html/body/main/article/section/div/div/section[2]/div[2]/div/h1/text()').get()
        print(elemento)

MySpider().start_requests()