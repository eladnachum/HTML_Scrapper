import urllib2
import sys
from optparse import OptionParser
from pip._vendor.requests import RequestException
import requests
from lxml import html
from lxml import etree

from BeautifulSoup import BeautifulSoup


# Request
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Accept-Language": "en-US,en;q=0.8",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
}


main_url=""
site_url = "https://www.amazon.com"
search_uri="/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords="
search_next_page=""


def makeRequest(findString, mainASIN):
    try:
        response = requests.get(main_url,headers=headers)
        print main_url


        """myparser = etree.HTMLParser(encoding="ascii")
        tree = etree.HTML(response.text, parser=myparser)"""

        tree = html.fromstring(response.content)
        """for i in tree.iterchildren():
            print i"""

        global search_next_page
        #nextPage = tree.get_element_by_id('pagnNextLink')
        nextPage=tree.xpath('//a[@id="pagnNextLink"]')
        #nextPage=tree.xpath('//div')
        #nextPage=tree.xpath('//*')

        search_next_page=nextPage[0].attrib['href']

        #page_results = tree.xpath('//ul[@id="s-results-list-atf"]//li') # get all the results from the page.
        page_results = tree.xpath('//li') # get all the results from the page.
        for child in page_results:
            try:
                tempASIN=child.attrib['data-asin'] # get data asin of the current product
                if tempASIN == mainASIN:
                    return True
            except:
                pass
    except RequestException as e:
        print "WARNING: Request for {} failed, trying again.".format(main_url)
    return False



def main():
    searchTillPage=10
    #print "Please enter a string to search for:"
    #findString=raw_input() # getting the string to look for
    #print "Please enter an ASIN code:"
    #mainASIN=raw_input() #get ASIN code.

    usage = "usage: %prog [options] arg"
    findString=""
    mainASIN=""
    parser = OptionParser(usage)
    parser.add_option("-s", "--string", dest="findString",
                      help="search amazon for the given string")
    parser.add_option("-a", "--ASIN",
                      dest="mainASIN", help="search for the given ASIN code")

    (options, args) = parser.parse_args()
    print options
    print args
    #if len(args) < 2:
     #   parser.error("incorrect number of arguments")
    #elif len(args)==2:
    if options.findString is not None and options.mainASIN is not None:
        global main_url
        global search_next_page

        if args!=0:
            for a in args:
                options.findString=options.findString+ " " +a
        options.findString=options.findString.replace(" ","+") # prepare for search
        main_url = site_url + search_uri + options.findString # the main url to search

        for i in range(1,searchTillPage): # page counter
            ret=makeRequest(options.findString,options.mainASIN) # make request with pag
            if ret:
                print i
                return i
            main_url=site_url+search_next_page
        return "Not exist in the first 10 pages"
    else:
        parser.error("incorrect number of arguments")

if __name__ == "__main__":
    main()