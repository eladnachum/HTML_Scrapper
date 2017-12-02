import urllib2
import requests
from lxml import html
import json
import unicodedata
from Apartment import Apartment

def toInt (price):
       return int(price.replace(',', ''))

def price_to_int (price):
       return int(price[3:].replace(',',''))

def toHebrew (str):
       if (str): return ''.join(chr(ord(c)) for c in str)


def extractSpanText(tree, element_id):
       element = tree.xpath('//span[@id="%s"]'%element_id)
       if (element):
              return element[0].text
       else: return ""


hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}


filters = {
            'multiSearch':'1',
            'City':'%FA%EC+%E0%E1%E9%E1+%E9%F4%E5',
            'Neighborhood':'%E4%F6%F4%E5%EF+%E4%E7%E3%F9-+%F6%F4%E5%EF',
            'HomeTypeID':'1',
            'fromRooms':'',
            'untilRooms':'',
            'fromPrice':'500000',
            'untilPrice':'2250000',
            'PriceType':'1',
            'fromSquareMeter':'45',
            'untilSquareMeter':'',
            'FromFloor':'',
            'ToFloor':'',
            'Info':'',
            'PriceOnly':'1'
           }

yad2_url = "http://www.yad2.co.il/Nadlan/sales.php"
yad2_url_with_query = yad2_url+"?multiSearch=1&City=%FA%EC+%E0%E1%E9%E1+%E9%F4%E5&Neighborhood=%E4%F6%F4%E5%EF+%E4%E7%E3%F9-+%F6%F4%E5%EF&HomeTypeID=1&fromRooms=&untilRooms=&fromPrice=500000&untilPrice=2250000&PriceType=1&fromSquareMeter=45&untilSquareMeter=&FromFloor=&ToFloor=&Info=&PriceOnly=1"
from selenium.webdriver.common.proxy import *
from bs4 import BeautifulSoup
from selenium import webdriver

from browsermobproxy import Server
server = Server("path/to/browsermob-proxy")
server.start()
proxy = server.create_proxy()

myProxy = "http://genproxy.corp.amdocs.com:8080"
proxy = Proxy({
    'proxyType': ProxyType.AUTODETECT
    })

driver = webdriver.Firefox(proxy=proxy)
driver.get(yad2_url_with_query)

html = driver.page_source
soup = BeautifulSoup(html)


res = requests.get(yad2_url,headers=hdr,params=filters)
print "hi"