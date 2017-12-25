#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#####
#README
# maybe try to take the start date and end date and do it by months and not at once...
#####


#import urllib
import requests
from lxml import html
import json
import sys
import datetime
from helper import HAR_to_dict
from helper import get_requests_from_HAR_file
from datetime import timedelta, date

#returns all dates between start_data and end_date (implicit end_date)
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def handle_conditions_string(conditions_string):
        codes = {'FEW': 1.5,'SCT': 3.5,'BKN': 6,'OVC': 8}
        for code in codes:
          if code in conditions_string:
            return codes[code]
        return None

#get daily/hourly data for each day 
def get_weather_daily_data(date_str):
  my_request['url'] = 'https://www.wunderground.com/history/airport/LLBG/{date_str}/DailyHistory.html'.format(date_str=date_str)
  my_request['headers'] = HAR_to_dict(manual_requests[0]['request']['headers'])
  my_request['cookies'] = HAR_to_dict(manual_requests[0]['request']['cookies'])

  response = requests.get(url=my_request['url'], headers=my_request['headers'], cookies=my_request['cookies'])
  tree = html.fromstring(response.content)

  #key: time(hour), value: dict of data (see list of fields)
  daily_data = {}
  fields = ['Time','Temp','DewPoint','Humidity','Pressure','Visibility','WindDir','WindSpeed','GustSpeed','Precip','Events','Conditions']
  fields_xpath_suffixes = ['td[1]','td[2]/span/span[1]','td[3]/span/span[1]','td[4]','td[5]/span/span[1]','td[6]','td[7]','td[8]/span[1]/span[1]','td[9]','td[10]','td[11]','td[12]']

  #loop over rows
  row_num=1
  while(tree.xpath('//*[@id="obsTable"]/tbody/tr[{row_num}]'.format(row_num=row_num))):
      data = {}
      for field,field_xpath_suffix in zip(fields,fields_xpath_suffixes):
          xpath = '//*[@id="obsTable"]/tbody/tr[{row}]/{xpath_suffix}'.format(row=row_num,xpath_suffix=field_xpath_suffix)
          try:
              data[field] = tree.xpath(xpath)[0].text
          except:
              raise
      #handle conditions string
      conditions_string = tree.xpath('//*[@id="obsTable"]/tbody/tr[{row}]/td[2]'.format(row=row_num+1))[0].text
      if data['Conditions'] != "Clear":
        code = handle_conditions_string(conditions_string)
      else:
        code = 0
      data['conditions_details'] = {'code': code,'str': conditions_string}
      
      daily_data[data['Time']] = data
      row_num = row_num + 2

  #calculate conditions average
  sum = 0
  len = 0
  i = 0
  for time in daily_data.values():
    i = i +1
    if time['conditions_details']['code'] is not None: 
      sum = sum + time['conditions_details']['code']
      len = len +1
  print i
  print sum
  print len
  return sum/len

  return daily_data


def get_weather_monthly_data(month,year):
  from time import strptime

  my_request['url'] = "https://www.wunderground.com/history/airport/LLBG/{year}/{month}/1/MonthlyHistory.html?&reqdb.zip=&reqdb.magic=&reqdb.wmo=".format(month=month,year=year)
  my_request['headers'] = HAR_to_dict(manual_requests[0]['request']['headers'])
  my_request['cookies'] = HAR_to_dict(manual_requests[0]['request']['cookies'])

  response = requests.get(url=my_request['url'], headers=my_request['headers'], cookies=my_request['cookies'])
  tree = html.fromstring(response.content)

  #check we got the right mothly info  
  page_year = tree.xpath('//*[@id="obsTable"]/thead/tr/th[1]')[0].text
  page_month = tree.xpath('//*[@id="obsTable"]/tbody[1]/tr/td[1]')[0].text
  if ((month != strptime(page_month,'%b').tm_mon) or (int(page_year) != year)):
    print "Error. Got wrong month/year ({page_month}/{page_year}) instead of {month}/{year}".format(month=month,year=year,page_year=page_year,page_month=page_month)
    return None
  
  #loop over rows (days)
  fields = ['Temp','DewPoint','Humidity','SeaLevelPress','Visibility','Wind','Precip','Events']
  fields_xpath_suffixes = ['td[3]/span','td[6]/span','td[9]/span','td[12]/span','td[15]/span','td[18]/span','td[20]/span','td[21]']
  data = {}

  idx = 2
  while (True):
    day_elem = tree.xpath('//*[@id="obsTable"]/tbody[{row}]/tr/td[1]/a'.format(row=idx))
    #if empty => no more days
    if (not day_elem):
      break
    
    day = day_elem[0].text

    day_data={}
    for field,field_xpath_suffix in zip(fields,fields_xpath_suffixes):
          xpath = '//*[@id="obsTable"]/tbody[{row}]/tr/{xpath_suffix}'.format(row=idx,xpath_suffix=field_xpath_suffix)
          try:
            day_data[field]=tree.xpath(xpath)[0].text.replace('&nbsp;',' ')
          except:
              raise
    
    data[day] = day_data
    idx = idx + 1

  return data








#get daily data for range of dates
def get_weather_data(start_date_str,end_date_str):
  end_date_arr = end_date_str.split('/')
  my_request['url'] = "https://www.wunderground.com/history/airport/LLBG/{start_date_str}/CustomHistory.html?dayend={end_day}&monthend={end_month}&yearend={end_year}&req_city=&req_state=&req_statename=&reqdb.zip=&reqdb.magic=&reqdb.wmo=".format(start_date_str=start_date_str,end_year=end_date_arr[0],end_month=end_date_arr[1],end_day=end_date_arr[2])
  my_request['headers'] = HAR_to_dict(manual_requests[0]['request']['headers'])
  my_request['cookies'] = HAR_to_dict(manual_requests[0]['request']['cookies'])

  response = requests.get(url=my_request['url'], headers=my_request['headers'], cookies=my_request['cookies'])
  tree = html.fromstring(response.content)
  
  fields = ['Temp','DewPoint','Humidity','SeaLevelPress','Visibility','Wind','Precip','Events']



  a = tree.xpath(xpath)
  print a[0].attrib['href']
  print a[0].text


  #loop over rows
  row_num=1
  curr_year = int(tree.xpath('//*[@id="obsTable"]/thead[1]/tr/th[1]'))
  curr_month = 1
  while(True):
    first_field = tree.xpath('//*[@id="obsTable"]/tbody[{row_num}]/tr/td[1]/a'.format(row_num=row_num))
    if (not first_field):
      #means it's a new month (regular td instead of a-href)
      if curr_month == 12:
        curr_year = curr_year + 1
      else:
        curr_month = curr_month + 1

    else:
      #means it's a regular day line
      row_data = {}
      for col_indx,field in enumerate(fields):
        date_key = "{year}/{month}/{day}".format(year=curr_year,month=curr_month,day=first_field[0].text)
        val = tree.xpath('//*[@id="obsTable"]/tbody[{row_num}]/tr/td[{col}]'.format(row_num=row_num,col=col_indx))
        #row_data[date_key].update(fields[i]: val)


  return



########
# MAIN #
########

manual_requests = get_requests_from_HAR_file('HARS/DailyHistory.json')
my_request = {}
weather_data = {}


start_date = date(2016, 12, 5)
end_date = date(2017, 1, 7)

from dateutil.relativedelta import relativedelta
date = start_date
while date < end_date:
  date_key = "{year}/{month}".format(year=date.year,month=date.month)
  weather_data[date_key] = get_weather_monthly_data(date.month,date.year)
  date += relativedelta(months=1)

print json.dumps(weather_data,indent=4)
sys.exit()

#get history data
get_weather_data("2016/1/3","2017/2/4")


#get daily conditions (for clouds)
for single_date in daterange(start_date, end_date):
  date_str = single_date.strftime("%Y/%m/%d")
  weather_data[date_str] = get_weather_daily_data(date_str)

print json.dumps(weather_data,indent=4)

