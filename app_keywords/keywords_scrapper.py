import urllib2
import requests
from lxml import html
import json
from helper import HAR_to_dict
import sys, os
import time
from multiprocessing import Pool


def remove_keys(the_dict,keys):
  for key in keys:
    del the_dict[key]

def load_words(relative_path):
    try:
        filename = os.path.abspath(relative_path)+"\\"+"words_dictionary.json"
        with open(filename,"r") as english_dictionary:
            valid_words = json.load(english_dictionary)
            return valid_words
    except Exception as e:
        return None

def load_words_simple_file(relative_path):
    try:
       filename = os.path.abspath(relative_path)+"\\"+"input.txt"
       with open(filename,"r") as input_file:
           return [line.strip() for line in input_file.readlines()]
           
    except Exception as e:
        return None

# Get: a keyword
# Action: Adds the keyword to "my keywords" in the website
def set_my_keywords(keyword=None,os_version='android'): 
  ios_headers_for_add_keyword_HAR =  [
            {
              "name": "Cookie",
              "value": "__uvt=; _ga=GA1.2.873370462.1510860176; intercom-id-pjtwd42d=cbbd47f7-be1f-4db9-9f3a-86593757378c; mp_f9c053f6cb8aa27c2fe7abfb4847484a_mixpanel=%7B%22distinct_id%22%3A%20%2215fc65ea98426b-07d4a50c6429e1-3b3e5906-15f900-15fc65ea98510d%22%2C%22utm_source%22%3A%20%22searchman%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fsearchman.com%2Fios%2Fapp%2Fus%2F493253309%2Fen%2Fblockchain%2Fblockchain-bitcoin-wallet%2F%3Fd%3DiPhone%22%2C%22%24initial_referring_domain%22%3A%20%22searchman.com%22%7D; ag_uh=3a435e642830ef73bee7e0e0d5ed1358; ag_uhc=75b60a7055763f595e1d3e899bc578ed; ag-portfolio=%5B%22ios-886427730%22%5D; ag_bh=806719182%3AUS%2C1291851950%3AUS%2C1023123599%3AUS%2C868077558%3AUS%2Cio.voodoo.dune%3AUS%2C915637540%3AUS%2C886427730%3AUS%2C493253309%3AUS%2C; ag_lang=en; ag_public_imps=21; __utmt=1; __utma=247563269.873370462.1510860176.1511200723.1511203314.8; __utmb=247563269.6.10.1511203314; __utmc=247563269; __utmz=247563269.1510860176.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); mp_2b6156b771e3a1688ea2424a5f3e5aba_mixpanel=%7B%22distinct_id%22%3A%20%22100923%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fsearchman.com%2Fsignin%3Fnext%3D%252F%22%2C%22%24initial_referring_domain%22%3A%20%22searchman.com%22%2C%22__mps%22%3A%20%7B%7D%2C%22__mpso%22%3A%20%7B%7D%2C%22__mpus%22%3A%20%7B%7D%2C%22__mpa%22%3A%20%7B%7D%2C%22__mpu%22%3A%20%7B%7D%2C%22__mpap%22%3A%20%5B%5D%7D; uvts=6lwMqzNSEByfwHAD; __stripe_sid=a39cba9b-8469-49a0-a8fa-1c5903e0a120; __stripe_mid=2a7dca9a-3c7e-463c-ab35-80d4cb4b798e; mp_mixpanel__c=5"
            },
            {
              "name": "Origin",
              "value": "https://searchman.com"
            },
            {
              "name": "Accept-Encoding",
              "value": "gzip, deflate, br"
            },
            {
              "name": "Host",
              "value": "searchman.com"
            },
            {
              "name": "Accept-Language",
              "value": "en-US,en;q=0.9,he;q=0.8"
            },
            {
              "name": "User-Agent",
              "value": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
            },
            {
              "name": "Content-Type",
              "value": "application/x-www-form-urlencoded; charset=UTF-8"
            },
            {
              "name": "Accept",
              "value": "application/json, text/javascript, */*; q=0.01"
            },
            {
              "name": "Referer",
              "value": "https://searchman.com/ios/my_keywords/886427730/US/"
            },
            {
              "name": "X-Requested-With",
              "value": "XMLHttpRequest"
            },
            {
              "name": "Connection",
              "value": "keep-alive"
            },
            {
              "name": "Content-Length",
              "value": "31"
            }
          ]
  android_headers_for_add_keyword_HAR = [
            {
              "name": "Cookie",
              "value": "__uvt=; _ga=GA1.2.873370462.1510860176; intercom-id-pjtwd42d=cbbd47f7-be1f-4db9-9f3a-86593757378c; mp_f9c053f6cb8aa27c2fe7abfb4847484a_mixpanel=%7B%22distinct_id%22%3A%20%2215fc65ea98426b-07d4a50c6429e1-3b3e5906-15f900-15fc65ea98510d%22%2C%22utm_source%22%3A%20%22searchman%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fsearchman.com%2Fios%2Fapp%2Fus%2F493253309%2Fen%2Fblockchain%2Fblockchain-bitcoin-wallet%2F%3Fd%3DiPhone%22%2C%22%24initial_referring_domain%22%3A%20%22searchman.com%22%7D; ag_uh=3a435e642830ef73bee7e0e0d5ed1358; ag_uhc=75b60a7055763f595e1d3e899bc578ed; ag-portfolio=%5B%22ios-886427730%22%5D; __utmt=1; ag_public_imps=23; ag_lang=en; ag_bh=com.coinbase.android%3AUS%2C806719182%3AUS%2C1291851950%3AUS%2C1023123599%3AUS%2C868077558%3AUS%2Cio.voodoo.dune%3AUS%2C915637540%3AUS%2C886427730%3AUS%2C493253309%3AUS%2C; __utma=247563269.873370462.1510860176.1511250766.1511261486.11; __utmb=247563269.7.10.1511261486; __utmc=247563269; __utmz=247563269.1510860176.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); mp_2b6156b771e3a1688ea2424a5f3e5aba_mixpanel=%7B%22distinct_id%22%3A%20%22100923%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fsearchman.com%2Fsignin%3Fnext%3D%252F%22%2C%22%24initial_referring_domain%22%3A%20%22searchman.com%22%2C%22__mps%22%3A%20%7B%7D%2C%22__mpso%22%3A%20%7B%7D%2C%22__mpus%22%3A%20%7B%7D%2C%22__mpa%22%3A%20%7B%7D%2C%22__mpu%22%3A%20%7B%7D%2C%22__mpap%22%3A%20%5B%5D%7D; uvts=6lwMqzNSEByfwHAD; __stripe_sid=fd046fe6-efa7-4687-83e3-81a441a00dc8; __stripe_mid=2a7dca9a-3c7e-463c-ab35-80d4cb4b798e; mp_mixpanel__c=6"
            },
            {
              "name": "Origin",
              "value": "https://searchman.com"
            },
            {
              "name": "Accept-Encoding",
              "value": "gzip, deflate, br"
            },
            {
              "name": "Host",
              "value": "searchman.com"
            },
            {
              "name": "Accept-Language",
              "value": "en-US,en;q=0.9,he;q=0.8"
            },
            {
              "name": "User-Agent",
              "value": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
            },
            {
              "name": "Content-Type",
              "value": "application/x-www-form-urlencoded; charset=UTF-8"
            },
            {
              "name": "Accept",
              "value": "application/json, text/javascript, */*; q=0.01"
            },
            {
              "name": "Referer",
              "value": "https://searchman.com/android/my_keywords/com.coinbase.android/US/"
            },
            {
              "name": "X-Requested-With",
              "value": "XMLHttpRequest"
            },
            {
              "name": "Connection",
              "value": "keep-alive"
            },
            {
              "name": "Content-Length",
              "value": "28"
            }
          ]
  ios_headers_for_add_keyword = HAR_to_dict(ios_headers_for_add_keyword_HAR)
  android_headers_for_add_keyword = HAR_to_dict(android_headers_for_add_keyword_HAR)

  ios_url_for_add_keyword = "https://searchman.com/ios/my_keywords_save/886427730/US"
  android_url_for_add_keyword = "https://searchman.com/android/my_keywords_save/com.coinbase.android/US"

  data = {'terms': keyword,'term_type': '3'}
  if os_version is 'android':
    response = requests.post(url=android_url_for_add_keyword,headers=android_headers_for_add_keyword,data=data)
  if os_version is 'ios':
    response = requests.post(url=ios_url_for_add_keyword,headers=ios_headers_for_add_keyword,data=data)

  #raise if response not ok
  response.raise_for_status()

# Get: a keyword
# Action: check for the score of the keyword
# Return: keyword's scores
def check_scores_by_keyword(keyword=None,os_version='android'):
  ios_headers = {
  'Host': 'searchman.com',
  'Connection': 'keep-alive',
  'Cache-Control': 'max-age=0',
  'Upgrade-Insecure-Requests': '1',
  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
  'Referer': 'https://searchman.com/ios/keyword_ranking_trends/886427730/US/',
  'Accept-Encoding': 'gzip, deflate, br',
  'Accept-Language': 'en-US,en;q=0.9,he;q=0.8',
  'Cookie': '__uvt=; _ga=GA1.2.873370462.1510860176; intercom-id-pjtwd42d=cbbd47f7-be1f-4db9-9f3a-86593757378c; mp_f9c053f6cb8aa27c2fe7abfb4847484a_mixpanel=%7B%22distinct_id%22%3A%20%2215fc65ea98426b-07d4a50c6429e1-3b3e5906-15f900-15fc65ea98510d%22%2C%22utm_source%22%3A%20%22searchman%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fsearchman.com%2Fios%2Fapp%2Fus%2F493253309%2Fen%2Fblockchain%2Fblockchain-bitcoin-wallet%2F%3Fd%3DiPhone%22%2C%22%24initial_referring_domain%22%3A%20%22searchman.com%22%7D; ag_uh=3a435e642830ef73bee7e0e0d5ed1358; ag_uhc=75b60a7055763f595e1d3e899bc578ed; ag-portfolio=%5B%22ios-886427730%22%5D; ag_bh=806719182%3AUS%2C1291851950%3AUS%2C1023123599%3AUS%2C868077558%3AUS%2Cio.voodoo.dune%3AUS%2C915637540%3AUS%2C886427730%3AUS%2C493253309%3AUS%2C; ag_lang=en; ag_public_imps=21; __utma=247563269.873370462.1510860176.1511089635.1511126607.5; __utmb=247563269.17.10.1511126607; __utmc=247563269; __utmz=247563269.1510860176.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); mp_2b6156b771e3a1688ea2424a5f3e5aba_mixpanel=%7B%22distinct_id%22%3A%20%22100923%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fsearchman.com%2Fsignin%3Fnext%3D%252F%22%2C%22%24initial_referring_domain%22%3A%20%22searchman.com%22%2C%22__mps%22%3A%20%7B%7D%2C%22__mpso%22%3A%20%7B%7D%2C%22__mpus%22%3A%20%7B%7D%2C%22__mpa%22%3A%20%7B%7D%2C%22__mpu%22%3A%20%7B%7D%2C%22__mpap%22%3A%20%5B%5D%7D; uvts=6lwMqzNSEByfwHAD; __stripe_sid=18b78061-ed8f-4ebe-a4c9-ee0d2abee991; __stripe_mid=2a7dca9a-3c7e-463c-ab35-80d4cb4b798e; mp_mixpanel__c=6'
  }

  android_headers = {
  'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
  'Accept-Encoding':'gzip, deflate, br',
  'Accept-Language':'en-US,en;q=0.9,he;q=0.8',
  'Cache-Control':'max-age=0',
  'Connection':'keep-alive',
  'Cookie':'__uvt=; _ga=GA1.2.873370462.1510860176; intercom-id-pjtwd42d=cbbd47f7-be1f-4db9-9f3a-86593757378c; mp_f9c053f6cb8aa27c2fe7abfb4847484a_mixpanel=%7B%22distinct_id%22%3A%20%2215fc65ea98426b-07d4a50c6429e1-3b3e5906-15f900-15fc65ea98510d%22%2C%22utm_source%22%3A%20%22searchman%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fsearchman.com%2Fios%2Fapp%2Fus%2F493253309%2Fen%2Fblockchain%2Fblockchain-bitcoin-wallet%2F%3Fd%3DiPhone%22%2C%22%24initial_referring_domain%22%3A%20%22searchman.com%22%7D; ag_uh=3a435e642830ef73bee7e0e0d5ed1358; ag_uhc=75b60a7055763f595e1d3e899bc578ed; ag-portfolio=%5B%22ios-886427730%22%5D; __utmt=1; ag_public_imps=23; ag_lang=en; ag_bh=com.coinbase.android%3AUS%2C806719182%3AUS%2C1291851950%3AUS%2C1023123599%3AUS%2C868077558%3AUS%2Cio.voodoo.dune%3AUS%2C915637540%3AUS%2C886427730%3AUS%2C493253309%3AUS%2C; __utma=247563269.873370462.1510860176.1511250766.1511261486.11; __utmb=247563269.8.10.1511261486; __utmc=247563269; __utmz=247563269.1510860176.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); mp_mixpanel__c=0; mp_2b6156b771e3a1688ea2424a5f3e5aba_mixpanel=%7B%22distinct_id%22%3A%20%22100923%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fsearchman.com%2Fsignin%3Fnext%3D%252F%22%2C%22%24initial_referring_domain%22%3A%20%22searchman.com%22%2C%22__mps%22%3A%20%7B%7D%2C%22__mpso%22%3A%20%7B%7D%2C%22__mpus%22%3A%20%7B%7D%2C%22__mpa%22%3A%20%7B%7D%2C%22__mpu%22%3A%20%7B%7D%2C%22__mpap%22%3A%20%5B%5D%7D; uvts=6lwMqzNSEByfwHAD; __stripe_sid=fd046fe6-efa7-4687-83e3-81a441a00dc8; __stripe_mid=2a7dca9a-3c7e-463c-ab35-80d4cb4b798e',
  'Host':'searchman.com',
  'Referer':'https://searchman.com/android/my_keywords/com.coinbase.android/US/',
  'Upgrade-Insecure-Requests':'1',
  'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
  }

  ios_url = "https://searchman.com/ios/keyword_ranking_trends/886427730/US/"
  android_url = "https://searchman.com/android/keyword_ranking_trends/com.coinbase.android/US/"

  if os_version is 'ios':
    response = requests.get(url=ios_url,headers=ios_headers)
  if os_version is 'android':
    response = requests.get(url=android_url,headers=android_headers)
  
  tree = html.fromstring(response.content)

  working_xpath = '//*[@id="page-content"]/div[6]'
  xpath = '//script[@id="search-ranking-iPhone"]/text()'
  android_xpath = '//script[@id="search-ranking-android"]/text()'
  volume = tree.xpath(android_xpath)
  script_html = volume[0].encode('utf-8')
  #print volume[0].attrib

  tree = html.fromstring(script_html)

  xpath = '//div[@class="sliding-container"]/table/tbody/tr'
  volume = tree.xpath(xpath)

  keywords = []
  volume_scores = []
  hits = []

  for tr in volume:
    keywords.append(tr.attrib['data-attr-keyword'])
  #print keywords
    #print "keyword: " + tr.attrib['data-attr-keyword']
    
  xpath_tag = xpath + '/td[2]/div'
  vol = tree.xpath(xpath_tag)

  for v in vol:
    #print v.attrib
    volume_scores.append(v.attrib['data-sort-value'])
    #print v.attrib['data-sort-value']

  xpath_tag = xpath + '/td[3]/div'
  hit = tree.xpath(xpath_tag)

  for h in hit:
    #print h.attrib
    hits.append(h.attrib['data-sort-value'])


  results = dict(zip(keywords,zip(volume_scores,hits)))
  try:
    keyword = "blaa"
    return"Keyword: %s  Volume: %s Hits: %s \n"%(keyword,results[keyword.lower()][0],results[keyword.lower()][1])
  except:
    print "Error. Can't find key %s. current keys: %s"%(keyword,results)
    sys.exit(1)

# call set and check
def check_keyword(keyword=None,os_version='android'):
  set_my_keywords(keyword)
  return check_scores_by_keyword(keyword)
  


###########################################################
# INIT
###########################################################

#english_words_dict = load_words("words")
english_words_dict = load_words_simple_file("words")
limit = -1

if english_words_dict is None:
  print "Error. Can't open or load the words file."
  sys.exit()

param_num = len(sys.argv)-1
if param_num is 0:
  print "Wrong parameters. Help:\n> %s OS_VERSION [LIMIT]"%sys.argv[0]
  sys.exit()
elif sys.argv[1] not in ['ios','android']:
  print "Wrong App Store Choose 'ios' or 'android'"
  sys.exit()  
elif param_num > 1:
  limit = int(sys.argv[2])

os_version = sys.argv[1]

#################################
# RESULTS FILE HANDLING
#################################

out_file_name = "output\\results_%s.txt"%time.strftime("%Y%m%d-%H%M%S")
out_file = open(out_file_name,mode='w',buffering=2)

print "Start checking words from english_dictionary...See live results in output file"
for keyword in english_words_dict:
  if limit == 0:
    sys.exit()
  res = check_keyword(keyword,os_version)
  #print res
  sys.stdout.flush()
  out_file.write(res)
  limit -= 1

out_file.close