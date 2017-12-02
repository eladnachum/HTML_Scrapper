import urllib2
import requests
from lxml import html
import json
from model.VirtualCoinPrice import VirtualCoinPrice
from AnalyzeEngine import AnalayzeEngine

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive',
       'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
       'Cookie': 'PHPSESSID=qcu7cddciiocf1cmm1r51b6j13; geoC=IL; StickySession=id.44536115289.144m.investing.com; optimizelyEndUserId=oeu1502438233664r0.7923769780697079; fpros_popup_mob=1502460369; _gat=1; _gat_allMobileSitesTracker=1; _gat_allSitesTracker=1; optimizelySegments=%7B%225799410008%22%3A%22gc%22%2C%225803260009%22%3A%22none%22%2C%225796780005%22%3A%22direct%22%2C%225793730061%22%3A%22false%22%7D; optimizelyBuckets=%7B%7D; _ga=GA1.2.219351785.1502438234; _gid=GA1.2.1547957594.1502438234; nyxDorf=Z2o3bWAoPmM2Y2FkZyo4OzRjNmo0LTIyMjA%3D',
       'Host': 'm.investing.com',
       'Origin': 'https://m.investing.com',
       'Referer': 'https://m.investing.com/currencies/btc-usd-historical-data',
       'X-Requested-With': 'XMLHttpRequest'
       }

vcoin_name = "neo"
#url for all coins history data
site_url = "https://coinmarketcap.com/currencies/{}/historical-data/".format(vcoin_name)

#url for main page
site_url = "https://m.investing.com/currencies/btc-usd-historical-data"
#array with the virtual coin data by date
data_array = []
#url for data services only
data_url = "https://m.investing.com/instrument/services/getHistoricalData"
html_prefix = '<!DOCTYPE html><html lang="en" dir="ltr" class="com"><head>dsd</head><body>'
html_suffix = '</body></html>'
# read data from file (True) or post a request (False)
offline = False

#if working in online mode
if not offline:
       response = requests.post(data_url,headers=hdr,data={'curr_id':'945629',
                                                           'st_date':'06/11/2013',
                                                           'end_date':'08/11/2017',
                                                           'interval_sec':'Daily'})

       tree = html.fromstring(html_prefix+response.content+html_suffix)
       row = 0
       while (True):
              row = row + 1
              #xpath lookup in the main page url
              #table_row = tree.xpath('//div[@id="siteWrapper"]/div[1]/section[3]/div[2]/div/div/table/tbody/tr[%d]/td' %row)
              table_row = tree.xpath('/html/body/div/div/table/tbody/tr[%d]/td'%row)
              if not table_row: break
              vcoin = VirtualCoinPrice(
                     date=table_row[0].text,
                     price=table_row[1].text,
                     open=table_row[2].text,
                     high=table_row[3].text,
                     low=table_row[4].text,
                     change=table_row[5].text)
              data_array.append(vcoin)
       #chaching data - writing to file
       with open('vcoin_data.txt', 'w') as outfile:
              for item in data_array:
                     json.dump(item.__dict__, outfile)
                     outfile.write("\n")
       outfile.close()
# else - working in offline mode
else:
       with open("vcoin_data.txt", 'r') as f:
              for line in f:
                     a = VirtualCoinPrice("none","none","none","none","none","none")
                     a.init_with_dict(json.loads(line))
                     data_array.append(a)
       f.close()




test = AnalayzeEngine(data_array)
res = test.calculate_seq_pattern(0,6)
print res




