import urllib2
import requests
from lxml import html
import json

phrase = "ella"

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

site_url = "http://transcripts.foreverdreaming.org"
main_endpoint = "/viewforum.php?f=189"

#####################################
#Getting all the episodes table pages
#####################################

main_url = site_url + main_endpoint
pages_urls = [main_url]
response = requests.get(main_url,headers=hdr)
tree = html.fromstring(response.content)
pages_hrefs = tree.xpath('//div[@id="wrapcentre"]/div[4]/div/div/b/a')
for page_href in pages_hrefs:
       endpoint = (page_href.attrib['href'])[1:]
       pages_urls.append(site_url + endpoint);


# Going through all the pages
for page_url in pages_urls:

       ################################
       # Getting the episodes urls
       ################################
       response = requests.get(page_url, headers=hdr)
       tree = html.fromstring(response.content)
       episodes_hrefs = tree.xpath('//div[@id="pagecontent"]/div[1]/div[2]/table/tr/td[1]/h3/a')
       episodes_urls = []
       for episode_href in episodes_hrefs:
              url = site_url + (episode_href.attrib['href'])[1:]
              episodes_urls.append(url)


       ##########################
       #Searching in each episode
       ##########################
       for episode_url in episodes_urls:
              response = requests.get(episode_url,headers=hdr)
              tree = html.fromstring(response.content)
              #script = tree.xpath('//div[@id="p125232"]/div/div[2]/p/text()')
              #script = tree.xpath('//div[@class="boxbody"]/div/div/div/div[2]/p/text()')
              script = tree.xpath('//div[@class="postbody"]/p/text()')
              episode = tree.xpath('//div[@id="pagecontent"]/div[1]/div[1]/h2/text()')

              print "Scanning Episode %s " % episode
              for line in script:
                     if phrase.lower() in line.lower():
                            print line




