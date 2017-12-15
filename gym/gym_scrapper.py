#!/usr/bin/env python
# -*- coding: utf-8 -*- 


import urllib
import requests
from lxml import html
import json
from helper import HAR_to_dict
import sys
import datetime


def lambda_handler(event,context):
  #check offline or online
  auth_flag = True
  write_to_file_flag = False
  return_dict = {}

  #authenticate
  auth_url="http://www.kolnoapeer.co.il/wp-content/themes/KolnoaPeer/inc/physical/login-handle.php"
  auth_headers_HAR=[
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
                "value": "http://www.kolnoapeer.co.il/"
              },
              {
                "name": "Cookie",
                "value": "optimizelyEndUserId=oeu1512829976741r0.20758536549030615; _hjIncludedInSample=1; optimizelySegments=%7B%225493192264%22%3A%22gc%22%2C%225520510180%22%3A%22false%22%2C%225515770230%22%3A%22search%22%7D; optimizelyBuckets=%7B%7D; _ga=GA1.3.644062575.1512829977; _gid=GA1.3.783463494.1513163597; _gat=1"
              },
              {
                "name": "Connection",
                "value": "keep-alive"
              },
              {
                "name": "Content-Length",
                "value": "38"
              }
            ]
  auth_headers=HAR_to_dict(auth_headers_HAR)
  auth_cookies_HAR = [
              {
                "name": "_ga",
                "value": "GA1.3.644062575.1512829977",
                "expires": None,
                "httpOnly": False,
                "secure": False
              },
              {
                "name": "_gat",
                "value": "1",
                "expires": None,
                "httpOnly": False,
                "secure": False
              },
              {
                "name": "_gid",
                "value": "GA1.3.783463494.1513163597",
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
                "name": "optimizelyBuckets",
                "value": "%7B%7D",
                "expires": None,
                "httpOnly": False,
                "secure": False
              },
              {
                "name": "optimizelyEndUserId",
                "value": "oeu1512829976741r0.20758536549030615",
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
              }
            ]
  auth_cookies = HAR_to_dict(auth_cookies_HAR)
  auth_data = {
              "mimeType": "application/x-www-form-urlencoded; charset=UTF-8",
              "text": "userEmail=0507609679&userPass=12345678",
              "params": [
                {
                  "name": "userEmail",
                  "value": "0507609679"
                },
                {
                  "name": "userPass",
                  "value": "12345678"
                }
              ]
            }
  auth_data="userEmail=0507609679&userPass=12345678"

  if (auth_flag):
    response = requests.post(url=auth_url,headers=auth_headers,data=auth_data)#,cookies=auth_cookies)
    auth_response_json = json.loads(response.content)
    session_token = auth_response_json['user_token']
  else:
    session_token = None


  #get weekly sched
  headers_HAR =  [
              {
                "name": "Cookie",
                "value": "optimizelyEndUserId=oeu1511636150491r0.03070219004762409; _hjIncludedInSample=1; peerUserLogged=true; peerUserID=14611; peerToken=3b5279c1775d41cabe6c0db93b0d7761; peerUserFirstName=%D7%90%D7%9C%D7%94; peerUserLastName=%D7%90%D7%9C%D7%A4%D7%A1%D7%99; peerUserEmail=alfasi21%40hotmail.com; peerUserPhone=%20; peerUserDetails=%7B%22status%22%3A%221%22%2C%22userid%22%3A14611%2C%22user_p_name%22%3A%22%5Cu05d0%5Cu05dc%5Cu05d4%22%2C%22user_token%22%3A%2272c424c0446f42f89bd3d5f4784fb391%22%2C%22user_l_name%22%3A%22%5Cu05d0%5Cu05dc%5Cu05e4%5Cu05e1%5Cu05d9%22%2C%22user_info%22%3A%7B%22CompanyID%22%3A201%2C%22BranchID%22%3A1%2C%22ID%22%3A14611%2C%22FirstName%22%3A%22%5Cu05d0%5Cu05dc%5Cu05d4%22%2C%22LastName%22%3A%22%5Cu05d0%5Cu05dc%5Cu05e4%5Cu05e1%5Cu05d9%22%2C%22MobilePhone%22%3A%22050-7609679%22%2C%22HomePhone%22%3A%22%20%22%2C%22WorkPhone%22%3A%22%20%22%2C%22CardNumber%22%3A0%2C%22Email%22%3A%22alfasi21%40hotmail.com%22%2C%22DateOfBirth%22%3A%221986-07-28T00%3A00%3A00%22%2C%22SignedRegulations%22%3Afalse%2C%22SignedRetulationsInt%22%3Anull%2C%22HasMedical%22%3Afalse%2C%22PaymentLeft%22%3A0%2C%22HasTrainingPlan%22%3Afalse%2C%22IsInsured%22%3Afalse%2C%22InsuranceEndDate%22%3Anull%2C%22CityName%22%3A%22%5Cu05ea%5Cu05dc%20%5Cu05d0%5Cu05d1%5Cu05d9%5Cu05d1%22%2C%22HouseNumber%22%3A0%2C%22GroupCode%22%3A0%2C%22IDNumber%22%3A21967583%2C%22NeighborhoodCode%22%3Anull%2C%22Cars%22%3A%7B%7D%7D%7D; optimizelySegments=%7B%225493192264%22%3A%22gc%22%2C%225520510180%22%3A%22false%22%2C%225515770230%22%3A%22search%22%7D; optimizelyBuckets=%7B%7D; _ga=GA1.3.462259338.1511636151; _gid=GA1.3.185880343.1511636151; _gat_UA-37156680-1=1"
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
  headers = HAR_to_dict(headers_HAR)

  #indicates which week to take from calander. [0/1] for [current/next week]. important to scheduling Sunday classes
  week_flag = 0
  url = "http://www.kolnoapeer.co.il/wp-content/themes/KolnoaPeer/inc/physical/weeklySched.php?week={week_flag}".format(week_flag=week_flag)

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

  cookies_HAR =  [
              {
                "name": "optimizelyEndUserId",
                "value": "oeu1512829976741r0.20758536549030615",
                "expires": None,
                "httpOnly": False,
                "secure": False
              },
              {
                "name": "_gat",
                "value": "1",
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
                "value": "GA1.3.644062575.1512829977",
                "expires": None,
                "httpOnly": False,
                "secure": False
              },
              {
                "name": "_gid",
                "value": "GA1.3.783463494.1513163597",
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
                "value": "3b5279c1775d41cabe6c0db93b0d7761",
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
                "value": "%7B%22status%22%3A%221%22%2C%22userid%22%3A14611%2C%22user_p_name%22%3A%22%5Cu05d0%5Cu05dc%5Cu05d4%22%2C%22user_token%22%3A%223b5279c1775d41cabe6c0db93b0d7761%22%2C%22user_l_name%22%3A%22%5Cu05d0%5Cu05dc%5Cu05e4%5Cu05e1%5Cu05d9%22%2C%22user_info%22%3A%7B%22CompanyID%22%3A201%2C%22BranchID%22%3A1%2C%22ID%22%3A14611%2C%22FirstName%22%3A%22%5Cu05d0%5Cu05dc%5Cu05d4%22%2C%22LastName%22%3A%22%5Cu05d0%5Cu05dc%5Cu05e4%5Cu05e1%5Cu05d9%22%2C%22MobilePhone%22%3A%22050-7609679%22%2C%22HomePhone%22%3A%22%20%22%2C%22WorkPhone%22%3A%22%20%22%2C%22CardNumber%22%3A0%2C%22Email%22%3A%22alfasi21%40hotmail.com%22%2C%22DateOfBirth%22%3A%221986-07-28T00%3A00%3A00%22%2C%22SignedRegulations%22%3Afalse%2C%22SignedRetulationsInt%22%3Anull%2C%22HasMedical%22%3Afalse%2C%22PaymentLeft%22%3A0%2C%22HasTrainingPlan%22%3Afalse%2C%22IsInsured%22%3Afalse%2C%22InsuranceEndDate%22%3Anull%2C%22CityName%22%3A%22%5Cu05ea%5Cu05dc%20%5Cu05d0%5Cu05d1%5Cu05d9%5Cu05d1%22%2C%22HouseNumber%22%3A0%2C%22GroupCode%22%3A0%2C%22IDNumber%22%3A21967583%2C%22ZipCode%22%3A0%2C%22NeighborhoodCode%22%3Anull%2C%22Cars%22%3A%7B%7D%7D%7D",
                "expires": None,
                "httpOnly": False,
                "secure": False
              }
            ]
  cookies = HAR_to_dict(cookies_HAR)


  #   request to auth_url returns a json with the user_token
  #   we take the token and injects it into our template cookie and header's cookie field
  cookies['peerToken'] = session_token
  headers ['Cookie'] = "optimizelyEndUserId=oeu1511636150491r0.03070219004762409; _hjIncludedInSample=1; peerUserLogged=true; peerUserID=14611; peerToken={session_token}; peerUserFirstName=%D7%90%D7%9C%D7%94; peerUserLastName=%D7%90%D7%9C%D7%A4%D7%A1%D7%99; peerUserEmail=alfasi21%40hotmail.com; peerUserPhone=%20; peerUserDetails=%7B%22status%22%3A%221%22%2C%22userid%22%3A14611%2C%22user_p_name%22%3A%22%5Cu05d0%5Cu05dc%5Cu05d4%22%2C%22user_token%22%3A%2272c424c0446f42f89bd3d5f4784fb391%22%2C%22user_l_name%22%3A%22%5Cu05d0%5Cu05dc%5Cu05e4%5Cu05e1%5Cu05d9%22%2C%22user_info%22%3A%7B%22CompanyID%22%3A201%2C%22BranchID%22%3A1%2C%22ID%22%3A14611%2C%22FirstName%22%3A%22%5Cu05d0%5Cu05dc%5Cu05d4%22%2C%22LastName%22%3A%22%5Cu05d0%5Cu05dc%5Cu05e4%5Cu05e1%5Cu05d9%22%2C%22MobilePhone%22%3A%22050-7609679%22%2C%22HomePhone%22%3A%22%20%22%2C%22WorkPhone%22%3A%22%20%22%2C%22CardNumber%22%3A0%2C%22Email%22%3A%22alfasi21%40hotmail.com%22%2C%22DateOfBirth%22%3A%221986-07-28T00%3A00%3A00%22%2C%22SignedRegulations%22%3Afalse%2C%22SignedRetulationsInt%22%3Anull%2C%22HasMedical%22%3Afalse%2C%22PaymentLeft%22%3A0%2C%22HasTrainingPlan%22%3Afalse%2C%22IsInsured%22%3Afalse%2C%22InsuranceEndDate%22%3Anull%2C%22CityName%22%3A%22%5Cu05ea%5Cu05dc%20%5Cu05d0%5Cu05d1%5Cu05d9%5Cu05d1%22%2C%22HouseNumber%22%3A0%2C%22GroupCode%22%3A0%2C%22IDNumber%22%3A21967583%2C%22NeighborhoodCode%22%3Anull%2C%22Cars%22%3A%7B%7D%7D%7D; optimizelySegments=%7B%225493192264%22%3A%22gc%22%2C%225520510180%22%3A%22false%22%2C%225515770230%22%3A%22search%22%7D; optimizelyBuckets=%7B%7D; _ga=GA1.3.462259338.1511636151; _gid=GA1.3.185880343.1511636151; _gat_UA-37156680-1=1".format(session_token=session_token)
  
  #get weekly sched
  if (auth_flag):
    response = requests.post(url=url,headers=headers,data=data,cookies=cookies)
    if (write_to_file_flag):
      weekly_sched_response_file = open('response.html','w')
      weekly_sched_response_file.write(response.content)
      weekly_sched_response_file.close()


  html_prefix = '<!DOCTYPE html><html lang="en" dir="ltr" class="com"><head>dsd</head><body>'
  html_suffix = '</body></html>'
  if (write_to_file_flag):
    with open("response.html") as weekly_sched_response_file:
      data=weekly_sched_response_file.read()
  else:
    data = response.content
  tree = html.fromstring(html_prefix+data+html_suffix)

  ###############################################################
  #xpath Examples:

  #xpath for all classes in specific day (1-7)
  #xpath = '/html/body/div/div[2]/article[6]/div'

  #xpath for the 8th class - for the number of seats section
  #xpath = '/html/body/div/div[2]/article[5]/div[8]/section[2]'

  #xpath for the 2th lesson - for the lesson name
  #xpath = '/html/body/div/div[2]/article[6]/div[2]/h4'
  ###############################################################

  #get all classes of DAY_NUMBER
  i = 0
  week_day = (datetime.datetime.today().weekday() + 3) % 7
  if week_day is 0:
    week_day = 7

  xpath = '/html/body/div/div[2]/article[{week_day}]/div'.format(week_day=week_day)
  lessons = tree.xpath(xpath)

  #looping over all lessons for tomorrow
  while (True):
    lesson = lessons[i]
    i = i +1
    xpath = '/html/body/div/div[2]/article[{week_day}]/div[{lesson_number}]/h4'.format(week_day=week_day,lesson_number=i)
    lesson_name = tree.xpath(xpath)[0].text
    #xpath = '/html/body/div/div[2]/article[{week_day}]/div[{lesson_number}]/section[2]'.format(week_day=week_day,lesson_number=i)
    #lesson_status = tree.xpath(xpath)[0].text

    date = lesson.attrib['data-date']
    xdate = urllib.quote_plus(date)
    hour = lesson.attrib['data-hour']
    xhour = urllib.quote_plus(hour)
    lessonID = lesson.attrib['data-classid']
    xlessonID = urllib.quote_plus(lessonID)
    instructor = lesson.attrib['data-instructor'].encode('UTF-8')
    xinstructor = urllib.quote_plus(instructor)
    if lesson_name in ['Kickboxing','Hiit Trx']:
      return_dict['lesson'] = lesson_name
      break

  #attrib = {'data-classid': '81', 'data-dur': '50', 'data-hour': '073000', 'data-date': '2017-12-14T07:30:00+02:00', 'data-instructor': u'\xd7\x9c\xd7\x99\xd7\xa8\xd7\x95\xd7\x9f \xd7\x9c.', 'class': 'one-course '}
  #<div class="one-course " data-classid="385" data-date="2017-12-15T09:00:00+02:00" data-hour="090000" data-dur="90" data-instructor="לינור מ.">

  #sign up to class
  request = {
            "method": "POST",
            "url": "http://www.kolnoapeer.co.il/wp-content/themes/KolnoaPeer/inc/physical/signToClass.php",
            "httpVersion": "HTTP/1.1",
            "headers": "ERASED",
            "queryString": [],
            "cookies": "ERASED",
            "headersSize": 2234,
            "bodySize": 114,
            "postData": {
              "mimeType": "application/x-www-form-urlencoded; charset=UTF-8",
              "text": "date=2017-12-15T09%3A00%3A00%2B02%3A00&hour=090000&lessonID=385&myInstructor=%D7%9C%D7%99%D7%A0%D7%95%D7%A8%20%D7%9E.",
              "params": [
                {
                  "name": "date",
                  "value": "2017-12-15T09%3A00%3A00%2B02%3A00"
                },
                {
                  "name": "hour",
                  "value": "090000"
                },
                {
                  "name": "lessonID",
                  "value": "385"
                },
                {
                  "name": "myInstructor",
                  "value": "%D7%9C%D7%99%D7%A0%D7%95%D7%A8%20%D7%9E."
                }
              ]
            }
          }
  url = request['url']
  data = "date={date}&hour={hour}&lessonID={lessonID}&myInstructor={myInstructor}".format(date=xdate,hour=xhour,lessonID=xlessonID,myInstructor=xinstructor)
  return_dict['form_data'] = data

  response = requests.post(url=url,headers=headers,cookies=cookies,data=data)
  return_dict['response_content'] = response.content
  return_dict['response_status_code'] = response.status_code
  #if response.content == 'success' and response.status_code is 200:
  #    return "signup for class succeed"
  #else:
  return return_dict



