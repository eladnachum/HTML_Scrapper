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
from datetime import timedelta, date, datetime



#returns all dates between start_data and end_date (implicit end_date)
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def handle_conditions_string(conditions_string):
        num = 0
        sum = 0.0
        codes = {'FEW': 1.5,'SCT': 3.5,'BKN': 6.0,'OVC': 8.0}
        for code in codes:
          if code in conditions_string:
            sum += codes[code]
            num +=1
        if sum == 0 or sum is None:
          return None
        else:
          return sum/num

def handle_conditions_column_string(conditions_string):
        if conditions_string == "" or conditions_string is None:
          return None

        #conditions_codes = {'Clear': 8,'Scattered Clouds':  7,'Mostly Cloudy':   5,'Partly Cloudy':   6,'Mist':  6,'Haze':  6,'Overcast':  5.5,'Unknown':   6.5,'Light Rain':  4.5,'Rain Showers':  3.5,'Light Thunderstorms and Rain':  2.5,'Thunderstorms and Rain':  2,'Thunderstorm':  2,'Rain':  4,'Light Drizzle':   5,'Patches of Fog':  6,'Snow':  3,'Heavy Rain': 2, 'Drizzle': 5}
        conditions_codes = csv_file_to_dict('conditions_codes.csv')
        return float(conditions_codes[conditions_string])
        
def handle_events_string(events_string):
        if events_string == "" or events_string is None:
          return 5
          
        num = 0
        sum = 0.0
        events_codes = {'Rain': 70.0,'Thunderstorm': 60.0,'Hail': 80.0, 'Snow': 90.0, 'Fog': 30.0}
        events = events_string.split(';')
        for event in events:
          if event in events_codes:
            sum += events_codes[event]
            num +=1
        if sum == 0 or sum is None:
          return None
        else:
          return sum/num

def csv_file_to_dict(file_name):
  import csv
  result={}
  with open(file_name,'r') as f:
      line = f.readline()
      while line:
        [k,v] = line.split(",")
        result[k]=v.strip()
        line = f.readline()
  return result

#key is date (2017/3/14). value is weather data dict. csv created columns are date and all data fields
def write_weather_dict_to_csv(weather_data,csv_file_name):
    import csv
    #weather_data={"date1":{"cl1":"v1","cl2":"v2","cl3":"v3"},"date2":{"cl1":"va","cl2":"vb","cl3":"vc"}}

    #list of fields names for the csv
    fieldnames = ['date']
    #add the data keys - the dict keys of each day
    fieldnames.extend(weather_data[weather_data.keys()[0]].keys())

    listWriter = csv.DictWriter(
       open(csv_file_name, 'wb'),
       fieldnames=fieldnames,
       delimiter=',',
       quotechar='|',
       quoting=csv.QUOTE_MINIMAL
    )

    #wrtie the columns names row
    listWriter.writerow(dict(zip(fieldnames,fieldnames)))

    #write all rows
    for k in weather_data:
        row = weather_data[k]
        row.update({"date":k})
        listWriter.writerow(row)


#get daily/hourly data for each day 
def get_weather_daily_data(date_str):
  manual_requests = get_requests_from_HAR_file('HARS/DailyHistory.json')
  my_request={}
  my_request['url'] = 'https://www.wunderground.com/history/airport/LLBG/{date_str}/DailyHistory.html'.format(date_str=date_str)
  my_request['headers'] = HAR_to_dict(manual_requests[0]['request']['headers'])
  my_request['cookies'] = HAR_to_dict(manual_requests[0]['request']['cookies'])

  response = requests.get(url=my_request['url'], headers=my_request['headers'], cookies=my_request['cookies'])
  tree = html.fromstring(response.content)

  #key: time(hour), value: dict of data (see list of fields)
  daily_data = {}
  fields = ['Time','Temp','DewPoint','Humidity','Pressure','Visibility','WindDir','WindSpeed','GustSpeed','Precip','Events','Conditions']
  fields_xpath_suffixes = ['td[1]','td[2]/span/span[1]','td[3]/span/span[1]','td[4]','td[5]/span/span[1]','td[6]','td[7]','td[8]/span[1]/span[1]','td[9]','td[10]','td[11]','td[12]']


  fields_titles = [th.text_content().strip() for th in tree.xpath('//*[@id="obsTable"]/thead/tr/th')]
  fields_xpath_suffixes = ['','td[2]/span/span[1]','td[3]/span/span[1]','td[4]','td[5]/span/span[1]','td[6]','td[7]','td[8]/span[1]/span[1]','td[9]','td[10]','td[11]','td[12]']

  #print [r.text_content().strip() for r in tree.xpath('//*[@id="obsTable"]/tbody/tr[3]/td')]
  #return
  #loop over rows
  row_num=1
  while(tree.xpath('//*[@id="obsTable"]/tbody/tr[{row_num}]'.format(row_num=row_num))):
      data = {}

      for idx,field in enumerate(fields_titles):
        try:
          xpath = '//*[@id="obsTable"]/tbody/tr[{row}]/td[{col}]/span/span[1]'.format(row=row_num,col=idx+1)
          data[field] = tree.xpath(xpath)[0].text
        except:          
          xpath = '//*[@id="obsTable"]/tbody/tr[{row}]/td[{col}]'.format(row=row_num,col=idx+1)
          data[field] = tree.xpath(xpath)[0].text

      #handle conditions string
      conditions_string = tree.xpath('//*[@id="obsTable"]/tbody/tr[{row}]/td[2]'.format(row=row_num+1))[0].text

      if data['Conditions'] != "Clear":
        code = handle_conditions_string(conditions_string)
      else:
        code = 0

      data['conditions_details'] = {'code': code,'str': conditions_string}
      
      daily_data[data[fields_titles[0]]] = data
      row_num = row_num + 2


  #calculate conditions average
  sum_str_code = 0.0
  sum_cond_code = 0.0
  len = 0
  i = 0
  for time in daily_data.values():
    i = i +1
    if time['conditions_details']['code'] is not None: 
      sum_str_code = sum_str_code + time['conditions_details']['code']
      sum_cond_code = sum_cond_code + handle_conditions_column_string(time['Conditions'])
      len = len +1

  return {'cond_str_code': sum_str_code/len, 'cond_code': sum_cond_code/len}


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
  
  data = {}
  fields = ['Day','Temp_H','Temp_A','Temp_M','DewPoint_H','DewPoint_A','DewPoint_M','Humidity_H','Humidity_A','Humidity_M','SeaLevelPress_H','SeaLevelPress_A','SeaLevelPress_M','Visibility_H','Visibility_A','Visibility_M','Wind_H','Wind_A','Wind_M','Precip','Events']
  #fields_xpath_suffixes = ['td[1]',td[3]/span','td[6]/span','td[9]/span','td[12]/span','td[15]/span','td[18]/span','td[20]/span','td[21]']
  
  idx = 2
  while (True):
    columns = [td.text_content().strip() for td in tree.xpath('//*[@id="obsTable"]/tbody[{row}]/tr/td'.format(row=idx))]
    if (not columns):
      break

    date_key = "{year}/{month}/{day}".format(year=year,month=month,day=columns[0])
    data[date_key] = dict(zip(fields,columns))
    idx = idx + 1  

  return data


def get_weather_custom_data(start_date,end_date):
  from time import strptime
  manual_requests = get_requests_from_HAR_file('HARS/DailyHistory.json')
  my_request={}
  start_date_str = "{year}/{month}/{day}".format(year=start_date.year,month=start_date.month,day=start_date.day)
  #my_request['url'] = "https://www.wunderground.com/history/airport/LLBG/{year}/{month}/1/MonthlyHistory.html?&reqdb.zip=&reqdb.magic=&reqdb.wmo=".format(month=month,year=year)
  my_request['url'] = "https://www.wunderground.com/history/airport/LLBG/{start_date_str}/CustomHistory.html?dayend={end_day}&monthend={end_month}&yearend={end_year}&req_city=&req_state=&req_statename=&reqdb.zip=&reqdb.magic=&reqdb.wmo=".format(start_date_str=start_date_str,end_year=end_date.year,end_month=end_date.month,end_day=end_date.day)
  my_request['headers'] = HAR_to_dict(manual_requests[0]['request']['headers'])
  my_request['cookies'] = HAR_to_dict(manual_requests[0]['request']['cookies'])

  response = requests.get(url=my_request['url'], headers=my_request['headers'], cookies=my_request['cookies'])
  tree = html.fromstring(response.content)
 
  data = {}
  fields = ['Day','Temp_H','Temp_A','Temp_M','DewPoint_H','DewPoint_A','DewPoint_M','Humidity_H','Humidity_A','Humidity_M','SeaLevelPress_H','SeaLevelPress_A','SeaLevelPress_M','Visibility_H','Visibility_A','Visibility_M','Wind_H','Wind_A','Wind_M','Precip','Events']
  #fields_xpath_suffixes = ['td[1]',td[3]/span','td[6]/span','td[9]/span','td[12]/span','td[15]/span','td[18]/span','td[20]/span','td[21]']
  
  months_dict = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
  idx = 1
  curr_month = None
  curr_year = start_date.year
  next_year_flag = False
  while (True):
    columns = [td.text_content().strip() for td in tree.xpath('//*[@id="obsTable"]/tbody[{row}]/tr/td'.format(row=idx))]
    if (not columns):
      break

    #check if its a month row
    if columns[0] in months_dict.keys():
      if next_year_flag is True:
        curr_year = str(int(curr_year) + 1)
        next_year_flag = False
      if columns[0] == 'Dec':
        next_year_flag = True
      curr_month = months_dict[columns[0]]
      idx += 1
      continue


    date_key = "{year}/{month}/{day}".format(year=curr_year,month=curr_month,day=columns[0])
    data[date_key] = dict(zip(fields,columns))
    cond_data = get_weather_daily_data(date_key)
    data[date_key]['ConditionsScore'] = cond_data['cond_code']
    data[date_key]['CloudsScore'] = cond_data['cond_str_code']
    data[date_key]['Events'] = handle_events_string(data[date_key]['Events'].replace("\t","").replace("\n","").replace(",",";"))

    #print date_key
    #print json.dumps(data[date_key],indent=4)
    #sys.stdout.flush()

    idx = idx + 1  

  return data



