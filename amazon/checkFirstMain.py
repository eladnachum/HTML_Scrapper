import urllib2
from pip._vendor.requests import RequestException
import requests
from lxml import html
from BeautifulSoup import BeautifulSoup


# Request
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Accept-Language": "en-US,en;q=0.8",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
}


headers_elad = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding":"gzip, deflate, br",
    "Accept-Language":"en-US,en;q=0.8,he;q=0.6",
    "Connection":"keep-alive",
    "Cookie":'x-wl-uid=19m4kzOtpnWJqS2O/cSAzVVYEDb+PjXmL/Q0q7Y1Xt6ZanUa0jur6rfSsWMdJZC+2cwMUBfDq0Uo=; session-token=sKGxN453BBvd8V0vBCkg/8E+JbzPH89R5U8w0eQLZwiCg9ogyIPgLaD4XaDbLD5wl9aEL+7kIH02CcKotn9WwhzL/anEAm6UTFuHQpucksVLxG/8gM3IV3DX2khCJ1UyWGHkGTdQ56/J9nac/PbaLXNG9mRIzTyK5fDQJ5QpIVfq4Z3KbTJnkNRpzzjJxzQ3qak1rYk5MfN5+TTRpaGLLegEAM1Ml7/UaUb9scZ2pE4ywnrVdC8q+Wbwg4zaDsHK; aws-target-static-id=1487489471842-40657; _mkto_trk=id:112-TZM-766&token:_mch-aws.amazon.com-1487489473275-10075; aws-business-metrics-last-visit=1497878097966; s_vn=1505721114959%26vn%3D27; c_m=undefinedwww.google.co.ilNatural%20Search; __utmz=194891197.1505053187.19.10.utmccn=(referral)|utmcsr=console.aws.amazon.com|utmcct=/console/home|utmcmd=referral; aws-ubid-main=163-3753862-2680314; aws-session-token="cWiIV9qVrMGfZOPXCqB7xSqdiAaGeZzUe0unolv1jGyU/x/+/6nvIci/5hZqHTjAs0cw3XldHsvt5XvU8AXyeHVkirjOAMU+4JrtSF6ghody+rfRnUycZD9L5eYK5SVc1KYJ49LaQDFcjdtf7DUJAQsfPpVaagqQzk6+8p37qo80IlBi94lmrB6ZTawnHKF1v7tLz5PZogHOq4XlmiyFAF4g/UYLqlC93pXhZi5Pty4="; aws-x-main="4DYkp62cBvIzgTsLw@O7j1LJsR8C0cotf0By4tKS@Mfq0UyAqhoNyl1?tJmZ2GEU"; aws-at-main=Atza|IwEBIOWlDH_FVd1vjKX1EZr8rBqesfgwpHS0AiKDCya6e9j3M4Gmw28yaH5hGL4AgJhhpOpb0qlHfeggrNTkFetVNdC0nMGA7bKeRgRDA6B8FChqqAit3yNlxo4ByWuwyx_PgxpUno9WGq_uO7jNCS2vqHB0Uy4cRTZfwLVKaO8PvKnowdmShMFNVVZE9WU-oRL0PGeWTmCBmD6GKmvUV0ZjOCqbLRbTQNHHU4eiv4WFBMAFN3LDOIlab-bO1UwNy8BLPK_W8rozugzw5sZVPFFDsVc8nZ-xF5cU5vVotujBznfJbfbz2U2JZNTLtZDf1XgdsEuYyTBa1Veq7btuSmIe4XjnQWZpq62Vop7oAqpDvR-s3O7ccxHHrdWyMrcPU_U7l9g0899ez2tTu8bgcKlSMMkBysj-f-3qOmw3ktyoS2N9PQ; sess-aws-at-main="nUYsIBO6kOIJVTdN1l1E6ZUV8oDVV5bqkuojSarRnl0="; aws-userInfo=%7B%22arn%22%3A%22arn%3Aaws%3Aiam%3A%3A314852337498%3Aroot%22%2C%22alias%22%3A%22%22%2C%22username%22%3A%22elad%22%2C%22keybase%22%3A%22nxo2X7rnyqTZJu1JGJWUk9d%2BXe5%2FlYKJ9rg%2FjG0yUWc%5Cu003d%22%2C%22issuer%22%3A%22https%3A%2F%2Fwww.amazon.com%2Fap%2Fsignin%22%7D; __utmv=194891197.%224DYkp62cBvIzgTsLw%40O7j1LJsR8C0cotf0By4tKS%40Mfq0UyAqhoNyl1%3FtJmZ2GEU%22; __utma=194891197.1024196377.1488096123.1505053187.1505053202.20; __utmc=194891197; aws-target-visitor-id=1487489471847-859317.26_22; aws-target-data=%7B%22support%22%3A%221%22%7D; s_fid=74E413CC94469FC7-07A4FCB56AEB34A3; s_dslv=1505054059023; s_nr=1505054059026-Repeat; regStatus=registered; s_cc=true; aws-session-id=144-7033516-5949522; aws-session-id-time=1505054089l; csm-hit=s-5GNZ47J9JM03NMKX9549|1505234369139; ubid-main=157-8202911-6880618; session-id-time=2082787201l; session-id=153-7549086-9875251',
    "Host":"www.amazon.com",
    "Upgrade-Insecure-Requests":1,
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
}

main_url=""
site_url = "https://www.amazon.com"
search_uri="/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords="
"""continue_search_uri_ref="/s/ref=sr_pg_"
continue_search_uri_fst1="?fst=p90x%3A1%2Cas%3Aon"
continue_search_uri_fst2="?fst=as%3Aon%2Cp90x%3A1"
continue_search_uri_rh="&rh=n%3A7141123011%2Ck%3A"
continue_search_uri_rh_inco="rh=i%3Aaps%2Ck%3A"
continue_search_uri_page=""
continue_search_uri_keywords="&keywords="
"""
search_next_page=""

#main_endpoint = "/viewforum.php?f=189"
#https://www.amazon.com/s/ref=sr_pg_2?fst=p90x%3A1%2Cas%3Aon&rh=n%3A7141123011%2Ck%3Ashoes&page=2&keywords=shoes&ie=UTF8&qid=1503089738&spIA=B07433CY79,B01NAWBXB7,B06VWC1C14
#https://www.amazon.com/gp/search/ref=sr_pg_3?fst=as%3Aon%2Cp90x%3A1&rh=n%3A7141123011%2Ck%3Ashoes&page=3&keywords=shoes&ie=UTF8&qid=1503089764&spIA=B07433CY79,B01NAWBXB7,B06VWC1C14,B01NAJ7ZR8,B01EYH40FA,B007XPEBAA
#https://www.amazon.com/s/ref=sr_pg_4?fst=p90x%3A1%2Cas%3Aon&rh=n%3A7141123011%2Ck%3Ashoes&page=4&keywords=shoes&ie=UTF8&qid=1503090033&spIA=B07433CY79,B01NAWBXB7,B06VWC1C14,B01NAJ7ZR8,B01EYH40FA,B007XPEBAA,B01G76V216,B01LZDRMAJ,B01EYH40HS
#https://www.amazon.com/s/ref=sr_pg_5?fst=as%3Aon%2Cp90x%3A1&rh=n%3A7141123011%2Ck%3Ashoes&page=5&keywords=shoes&ie=UTF8&qid=1503090259&spIA=B07433CY79,B01NAWBXB7,B06VWC1C14,B01NAJ7ZR8,B01EYH40FA,B007XPEBAA,B01G76V216,B01LZDRMAJ,B01EYH40HS,B01D8H6CYO,B01N27SN3W,B01N2TYGKC
#https://www.amazon.com/s/ref=nb_sb_ss_c_1_13?url=search-alias%3Daps&field-keywords=concrete+succulent+planter&sprefix=concrete+succ%2Caps%2C279&crid=3P4OKG7XA02PH

def beginCrawl(page,html,mainASIN):
    #print page
    subcategories = page.find("div",id="resultsCol")
    res = subcategories.findAll("li")

    global search_next_page
    nextPage=page.find("a",id="pagnNextLink")
    search_next_page=nextPage["href"]
    #print search_next_page

    for r in res: # for each item
        try:
            tempASIN=r["data-asin"]
            if tempASIN == mainASIN:
                return True
        except:
            pass
    return False
    #res = subcategories.find("li",id="result_0")


def makeRequest(findString, mainASIN):
    try:
        response = requests.get(main_url,headers=headers_elad)
        tree = html.fromstring(response.content)

        global search_next_page
        nextPage=tree.xpath('//a[@id="pagnNextLink"]')
        search_next_page=nextPage[0].attrib['href']

        page_results = tree.xpath('//ul[@id="s-results-list-atf"]/li') # get all the results from the page.
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
    #return isExistProduct


def makeReq(findString,mainASIN):
    #main_url = site_url + search_uri + findString+continue_search_uri_page
    #pages_urls = [main_url]
    try:
        #print main_url
        response = requests.get(main_url,headers=headers)
    except RequestException as e:
        print "WARNING: Request for {} failed, trying again.".format(main_url)
    isExistProduct=beginCrawl(BeautifulSoup(response.text), response.text,mainASIN)
    return isExistProduct


    #tree = html.fromstring(response.content)
    #print tree
    #page_searchtag = tree.xpath('//input[@id="twotabsearchtextbox"]') # getting the search object of amazon
    #print page_searchtag # need to search with a specific string.


def main():
    searchTillPage=10
    print "Please enter a string to search for:"
    findString=raw_input() # getting the string to look for
    print "Please enter an ASIN code:"
    mainASIN=raw_input() #get ASIN code.
    global main_url
    global search_next_page
    main_url = site_url + search_uri + findString
    findString=findString.replace(" ","+")
    #print main_url
    for i in range(1,searchTillPage): #page counter
        ret=makeReq(findString,mainASIN)# make request with pag
        if ret:
            print i
            return i
        main_url=site_url+search_next_page


if __name__ == "__main__":
    main()









