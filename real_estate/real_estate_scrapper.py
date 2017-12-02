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


price_limit = 2300000
relevant_ads_urls = []
sites = {}

Eshkol_site = {
       "url":"http://www.eshkol-nadlan.com",
       "ads_endpoint":"/search.aspx?agent=&sort=&sortDr=&typ=&pg="
}



#looping on all ads pages
page_index=0
while (True):
       print "testing page %d"%page_index
       site_ads_url = Eshkol_site['url'] + Eshkol_site['ads_endpoint'] + "%d"%page_index
       response = requests.get(site_ads_url, headers=hdr)
       tree = html.fromstring(response.content)
       #check if there are still ads in this page
       ads = tree.xpath('//div[@id="ctl06_guiGridBoxStrech1_Panel1"]/ul/li')
       if not ads: break
       ad_index = 0
       while (True):
              ad_index=ad_index+1
              ad_price_tag = tree.xpath('//div[@id="ctl06_guiGridBoxStrech1_Panel1"]/ul/li[%d]/div/a/span[1]'%ad_index)
              if not ad_price_tag: break
              ad_url_endpoint = tree.xpath('//div[@id="ctl06_guiGridBoxStrech1_Panel1"]/ul/li[%d]/div/div/p/a'%ad_index)
              price = price_to_int (ad_price_tag[0].text)
              if price <= price_limit:
                     relevant_ads_urls.append(Eshkol_site['url']+'/'+toHebrew(ad_url_endpoint[0].attrib['href']))
       page_index = page_index +1

Apartments = []
# looping over all the relevant ads
for ad_url in relevant_ads_urls:
       print "Checking ad in url: %s"%ad_url
       response = requests.get(ad_url, headers=hdr)
       tree = html.fromstring(response.content)
       apartment = Apartment(ad_url)
       #apartment.address = toHebrew(tree.xpath('//span[@id="ctl06_guiTofscarucel1_lblStreetData"]')[0].text)
       str = extractSpanText(tree,"ctl06_guiTofscarucel1_lblStreetData")
       apartment.address = toHebrew(str)
       apartment.neighborhood = toHebrew(tree.xpath('//span[@id="ctl06_guiTofscarucel1_lblShcunaData"]')[0].text)
       apartment.price = price_to_int(tree.xpath('//span[@id="ctl06_guiTofscarucel1_lblPriceData"]')[0].text)
       apartment.size = tree.xpath('//span[@id="ctl06_guiTofscarucel1_lblSqmrData"]')[0].text
       apartment.floor = tree.xpath('//span[@id="ctl06_guiTofscarucel1_lblFloorData"]')[0].text
       apartment.total_floors = tree.xpath('//span[@id="ctl06_guiTofscarucel1_lblFlooradData"]')[0].text
       apartment.rooms = tree.xpath('//span[@id="ctl06_guiTofscarucel1_lblRoomData"]')[0].text
       apartment.agent = "Agent"
       apartment.contact_name = "Eschkol Nadlan"
       apartment.contact_phone = "052-4750222  054-5454834  03-5445555"
       apartment.details = "Fetched from site"

       Apartments.append(apartment)


for apartment in Apartments: apartment.printMe()








##########################
#Searching in each episode
##########################
# for episode_url in episodes_urls:
#        response = requests.get(episode_url,headers=hdr)
#        tree = html.fromstring(response.content)
#        #script = tree.xpath('//div[@id="p125232"]/div/div[2]/p/text()')
#        #script = tree.xpath('//div[@class="boxbody"]/div/div/div/div[2]/p/text()')
#        script = tree.xpath('//div[@class="postbody"]/p/text()')
#        episode = tree.xpath('//div[@id="pagecontent"]/div[1]/div[1]/h2/text()')
#
#        print "Scanning Episode %s " % episode
#        for line in script:
#               if phrase.lower() in line.lower():
#                      print line
#



