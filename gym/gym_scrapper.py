import urllib2
import requests
from lxml import html
import json
from helper import HAR_to_dict


def browser_headers_parser(header_str,line_sep):
       #eader_str = "a:b\nc:d"
       res = (item.split(":") for item in header_str.split(line_sep))
       return dict(res)

hdr_str = {
       "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
       "Accept-Encoding":"gzip, deflate, sdch",
       "Accept-Language":"en-US,en;q=0.8,he;q=0.6",
       "Cookie":"optimizelyEndUserId=oeu1497092899464r0.713728219996405; _hjIncludedInSample=1; _gat=1; optimizelySegments=%7B%225493192264%22%3A%22gc%22%2C%225520510180%22%3A%22false%22%2C%225515770230%22%3A%22search%22%7D; optimizelyBuckets=%7B%7D; _ga=GA1.3.81796152.1497092900; _gid=GA1.3.1027390505.1498632389",
       "Host":"www.kolnoapeer.co.il",
       "Proxy-Connection":"keep-alive",
       "Referer":"https://www.google.co.il/",
       "Upgrade-Insecure-Requests":"1",
       "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

HAR =  [
            {
              "name": "Cookie",
              "value": "optimizelyEndUserId=oeu1511636150491r0.03070219004762409; _hjIncludedInSample=1; peerUserLogged=true; peerUserID=14611; peerToken=72c424c0446f42f89bd3d5f4784fb391; peerUserFirstName=%D7%90%D7%9C%D7%94; peerUserLastName=%D7%90%D7%9C%D7%A4%D7%A1%D7%99; peerUserEmail=alfasi21%40hotmail.com; peerUserPhone=%20; peerUserDetails=%7B%22status%22%3A%221%22%2C%22userid%22%3A14611%2C%22user_p_name%22%3A%22%5Cu05d0%5Cu05dc%5Cu05d4%22%2C%22user_token%22%3A%2272c424c0446f42f89bd3d5f4784fb391%22%2C%22user_l_name%22%3A%22%5Cu05d0%5Cu05dc%5Cu05e4%5Cu05e1%5Cu05d9%22%2C%22user_info%22%3A%7B%22CompanyID%22%3A201%2C%22BranchID%22%3A1%2C%22ID%22%3A14611%2C%22FirstName%22%3A%22%5Cu05d0%5Cu05dc%5Cu05d4%22%2C%22LastName%22%3A%22%5Cu05d0%5Cu05dc%5Cu05e4%5Cu05e1%5Cu05d9%22%2C%22MobilePhone%22%3A%22050-7609679%22%2C%22HomePhone%22%3A%22%20%22%2C%22WorkPhone%22%3A%22%20%22%2C%22CardNumber%22%3A0%2C%22Email%22%3A%22alfasi21%40hotmail.com%22%2C%22DateOfBirth%22%3A%221986-07-28T00%3A00%3A00%22%2C%22SignedRegulations%22%3Afalse%2C%22SignedRetulationsInt%22%3Anull%2C%22HasMedical%22%3Afalse%2C%22PaymentLeft%22%3A0%2C%22HasTrainingPlan%22%3Afalse%2C%22IsInsured%22%3Afalse%2C%22InsuranceEndDate%22%3Anull%2C%22CityName%22%3A%22%5Cu05ea%5Cu05dc%20%5Cu05d0%5Cu05d1%5Cu05d9%5Cu05d1%22%2C%22HouseNumber%22%3A0%2C%22GroupCode%22%3A0%2C%22IDNumber%22%3A21967583%2C%22NeighborhoodCode%22%3Anull%2C%22Cars%22%3A%7B%7D%7D%7D; optimizelySegments=%7B%225493192264%22%3A%22gc%22%2C%225520510180%22%3A%22false%22%2C%225515770230%22%3A%22search%22%7D; optimizelyBuckets=%7B%7D; _ga=GA1.3.462259338.1511636151; _gid=GA1.3.185880343.1511636151; _gat_UA-37156680-1=1"
            },
            {
              "name": "Origin",
              "value": "http://www.kolnoapeer.co.il"
            },
            {
              "name": "Accept-Encoding",
              "value": "gzip, deflate"
            },
            {
              "name": "Host",
              "value": "www.kolnoapeer.co.il"
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
              "value": "*/*"
            },
            {
              "name": "Referer",
              "value": "http://www.kolnoapeer.co.il/%d7%9e%d7%a2%d7%a8%d7%9b%d7%aa-%d7%97%d7%95%d7%92%d7%99%d7%9d-%d7%a9%d7%91%d7%95%d7%a2%d7%99/"
            },
            {
              "name": "X-Requested-With",
              "value": "XMLHttpRequest"
            },
            {
              "name": "Proxy-Connection",
              "value": "keep-alive"
            },
            {
              "name": "Content-Length",
              "value": "211"
            }
          ]
headers = HAR_to_dict(HAR)

url = "http://www.kolnoapeer.co.il/wp-content/themes/KolnoaPeer/inc/physical/weeklySched.php?week=1"

data =  {
            "mimeType": "application/x-www-form-urlencoded; charset=UTF-8",
            "text": "site_url=&permalink=http%3A%2F%2Fwww.kolnoapeer.co.il%2F%25d7%259e%25d7%25a2%25d7%25a8%25d7%259b%25d7%25aa-%25d7%2597%25d7%2595%25d7%2592%25d7%2599%25d7%259d-%25d7%25a9%25d7%2591%25d7%2595%25d7%25a2%25d7%2599%2F",
            "params": [
              {
                "name": "site_url",
                "value": ""
              },
              {
                "name": "permalink",
                "value": "http%3A%2F%2Fwww.kolnoapeer.co.il%2F%25d7%259e%25d7%25a2%25d7%25a8%25d7%259b%25d7%25aa-%25d7%2597%25d7%2595%25d7%2592%25d7%2599%25d7%259d-%25d7%25a9%25d7%2591%25d7%2595%25d7%25a2%25d7%2599%2F"
              }
            ]
          }

cookies_HAR = [
            {
              "name": "optimizelyEndUserId",
              "value": "oeu1511636150491r0.03070219004762409",
              "expires": None,
              "httpOnly": False,
              "secure": False
            },
            {
              "name": "_hjIncludedInSample",
              "value": "1",
              "expires": None,
              "httpOnly": False,
              "secure": False
            },
            {
              "name": "peerUserLogged",
              "value": "true",
              "expires": None,
              "httpOnly": False,
              "secure": False
            },
            {
              "name": "peerUserID",
              "value": "14611",
              "expires": None,
              "httpOnly": False,
              "secure": False
            },
            {
              "name": "peerToken",
              "value": "72c424c0446f42f89bd3d5f4784fb391",
              "expires": None,
              "httpOnly": False,
              "secure": False
            },
            {
              "name": "peerUserFirstName",
              "value": "%D7%90%D7%9C%D7%94",
              "expires": None,
              "httpOnly": False,
              "secure": False
            },
            {
              "name": "peerUserLastName",
              "value": "%D7%90%D7%9C%D7%A4%D7%A1%D7%99",
              "expires": None,
              "httpOnly": False,
              "secure": False
            },
            {
              "name": "peerUserEmail",
              "value": "alfasi21%40hotmail.com",
              "expires": None,
              "httpOnly": False,
              "secure": False
            },
            {
              "name": "peerUserPhone",
              "value": "%20",
              "expires": None,
              "httpOnly": False,
              "secure": False
            },
            {
              "name": "peerUserDetails",
              "value": "%7B%22status%22%3A%221%22%2C%22userid%22%3A14611%2C%22user_p_name%22%3A%22%5Cu05d0%5Cu05dc%5Cu05d4%22%2C%22user_token%22%3A%2272c424c0446f42f89bd3d5f4784fb391%22%2C%22user_l_name%22%3A%22%5Cu05d0%5Cu05dc%5Cu05e4%5Cu05e1%5Cu05d9%22%2C%22user_info%22%3A%7B%22CompanyID%22%3A201%2C%22BranchID%22%3A1%2C%22ID%22%3A14611%2C%22FirstName%22%3A%22%5Cu05d0%5Cu05dc%5Cu05d4%22%2C%22LastName%22%3A%22%5Cu05d0%5Cu05dc%5Cu05e4%5Cu05e1%5Cu05d9%22%2C%22MobilePhone%22%3A%22050-7609679%22%2C%22HomePhone%22%3A%22%20%22%2C%22WorkPhone%22%3A%22%20%22%2C%22CardNumber%22%3A0%2C%22Email%22%3A%22alfasi21%40hotmail.com%22%2C%22DateOfBirth%22%3A%221986-07-28T00%3A00%3A00%22%2C%22SignedRegulations%22%3Afalse%2C%22SignedRetulationsInt%22%3Anull%2C%22HasMedical%22%3Afalse%2C%22PaymentLeft%22%3A0%2C%22HasTrainingPlan%22%3Afalse%2C%22IsInsured%22%3Afalse%2C%22InsuranceEndDate%22%3Anull%2C%22CityName%22%3A%22%5Cu05ea%5Cu05dc%20%5Cu05d0%5Cu05d1%5Cu05d9%5Cu05d1%22%2C%22HouseNumber%22%3A0%2C%22GroupCode%22%3A0%2C%22IDNumber%22%3A21967583%2C%22NeighborhoodCode%22%3Anull%2C%22Cars%22%3A%7B%7D%7D%7D",
              "expires": None,
              "httpOnly": False,
              "secure": False
            },
            {
              "name": "optimizelySegments",
              "value": "%7B%225493192264%22%3A%22gc%22%2C%225520510180%22%3A%22false%22%2C%225515770230%22%3A%22search%22%7D",
              "expires": None,
              "httpOnly": False,
              "secure": False
            },
            {
              "name": "optimizelyBuckets",
              "value": "%7B%7D",
              "expires": None,
              "httpOnly": False,
              "secure": False
            },
            {
              "name": "_ga",
              "value": "GA1.3.462259338.1511636151",
              "expires": None,
              "httpOnly": False,
              "secure": False
            },
            {
              "name": "_gid",
              "value": "GA1.3.185880343.1511636151",
              "expires": None,
              "httpOnly": False,
              "secure": False
            },
            {
              "name": "_gat_UA-37156680-1",
              "value": "1",
              "expires": None,
              "httpOnly": False,
              "secure": False
            }
          ]
cookies = HAR_to_dict(cookies_HAR)

response = requests.post(url=url,headers=headers,data=data,cookies=cookies)
tree = html.fromstring(response.content)

print response.content
weekly_program = {'sunday':{},'monday':{},'thuesday':{},'wednsday':{},'thursday':{},'friday':{},'saturday':{}}


#xpath = '//*[@id="weekly-schedule"]/div[1]/div/div[2]/article[1]/div'
#classes = tree.xpath(xpath)
#print classes






# s = requests.session()
# #s.get(weekly_url,auth=('0507609679','12345678'))

# tree = html.fromstring(response.content)
# classes_sign_ups = tree.xpath('//section[@data-peer-status="available"]')

# #temp2 = classes_sign_ups[5].xpath('.//p')
# print classes_sign_ups
