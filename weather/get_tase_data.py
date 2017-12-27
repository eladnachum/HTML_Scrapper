#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import requests
from lxml import html
import json
import sys
import datetime
from helper import HAR_to_dict
from helper import get_requests_from_HAR_file
from datetime import timedelta, date
from dateutil.relativedelta import relativedelta


#output an html with all ISR stock data (not scrapped but can be opened in browser)
def get_all_stocks_data_html():
	return requests.get('http://www.tase.co.il/Heb/Management/GeneralPages/_layouts/Tase/ManagementPages/ExcelExport.aspx?sn=none&GridId=33&AddCol=1&Lang=he-IL&CurGuid={26F9CCE6-D184-43C6-BAB9-CF7848987BFF}&action=1&dualTab=&SubAction=0&date=&ExportType=1',verify=False).content

#output share/stock data by dates
def get_stock_data_by_dates(stock_id,company_id,from_date,to_date):
	#default values
	#company id and share/stock id can be extracted from the stock page in tase
	#for example: aaura stock. https://www.tase.co.il/Heb/General/Company/Pages/companyMainData.aspx?subDataType=0&companyID=000373&shareID=00373019
	company_id = "000373"
	share_id = "00373019"
	from_date = "01/01/2015"
	to_date= "01/06/2015"
	return requests.get("http://www.tase.co.il/_layouts/Tase/ManagementPages/Export.aspx?sn=none&GridId=128&ct=1&oid={share_id}&ot=1&lang=he-IL&cp=8&CmpId={company_id}&&ExportType=3&cf=0&cv=0&cl=0&cgt=1&dFrom={from_date}&dTo={to_date}".format(from_date=from_date,to_date=to_date,company_id=company_id,share_id=share_id),verify=False).content


#returns daily TA_125 data from start_date to end_date (implicit)
def get_TA125_by_dates(start_date,end_date):

	days_count = (end_date - start_date).days
	manual_requests = get_requests_from_HAR_file('HARS/bizportal_HAR.json')
	my_request = {}
	my_request['url'] = "http://www.bizportal.co.il/Quote/Transactions/HistoricalRates_AjaxBinding_Read/33333333?startD={s_day}%2F{s_mon}%2F{s_year}&endD={e_day}%2F{e_mon}%2F{e_year}&take={page_size}&skip=0&page=1&pageSize={page_size}&sort%5B0%5D%5Bfield%5D=DealDate&sort%5B0%5D%5Bdir%5D=desc".format(s_year=start_date.year,s_mon='{:02d}'.format(start_date.month),s_day='{:02d}'.format(start_date.day),e_year=end_date.year,e_mon='{:02d}'.format(end_date.month),e_day='{:02d}'.format(end_date.day),page_size=days_count)
	#my_request['url'] =	"http://www.bizportal.co.il/Quote/Transactions/HistoricalRates_AjaxBinding_Read/33333333?startD=10%2F03%2F2016&endD=26%2F03%2F2016&take={page_size}&skip=0&page=1&pageSize={page_size}&sort%5B0%5D%5Bfield%5D=DealDate&sort%5B0%5D%5Bdir%5D=desc".format(page_size=10)
	my_request['headers'] = HAR_to_dict(manual_requests[1]['request']['headers'])
	my_request['cookies'] = HAR_to_dict(manual_requests[1]['request']['cookies'])
	
	response = requests.get(url=my_request['url'], headers=my_request['headers'], cookies=my_request['cookies'], verify=False)
	json_str_content=response.content.replace('"', '\"')
	results = json.loads(json_str_content)
	print results['Errors']
	if results['Errors'] is None:
		return results['Data']
	else:
		return None
	

#methods that didn't work
def testing_tase_data():
	#####################################################################################################
	#trying with csv request - got stuck in the csv reader or maybe even the request itself is not good
	#####################################################################################################
	manual_requests = get_requests_from_HAR_file('HARS/tase_csv_request.json')
	my_request = {}
	my_request['url'] = manual_requests[0]['request']['url']
	my_request['headers'] = HAR_to_dict(manual_requests[0]['request']['headers'])
	my_request['cookies'] = HAR_to_dict(manual_requests[0]['request']['cookies'])
	#response = requests.get(url=my_request['url'], headers=my_request['headers'], cookies=my_request['cookies'], verify=False)#, queryString=my_request['queryString'])
	import csv 
	cr = csv.reader(open(my_request['url'],"rb"))
	for row in cr:
		print row

	sys.exit()

	############################################################################################
	#trying scrapping the html page...doen't work for some reason - maybe the script issue...
	############################################################################################
	manual_requests = get_requests_from_HAR_file('HARS/tase_HAR.json')
	my_request = {}
	cache_flag = True

	my_request['url'] = "https://www.tase.co.il/Heb/MarketData/Indices/MarketCap/Pages/IndexHistoryData.aspx?Action=3&addTab=&IndexId=137"
	my_request['headers'] = HAR_to_dict(manual_requests[0]['request']['headers'])
	my_request['cookies'] = HAR_to_dict(manual_requests[0]['request']['cookies'])
	my_request['queryString'] = HAR_to_dict(manual_requests[0]['request']['queryString'])
	my_request['postData'] = manual_requests[0]['request']['postData']['text']

	#print response.status_code
	#print response.content
	#sys.exit()

	html_content=None
	if (cache_flag is True):
		html_content = open('response.html','r').read()
	else:
		response = requests.post(url=my_request['url'], headers=my_request['headers'], cookies=my_request['cookies'], data=my_request['postData'], verify=False)#, queryString=my_request['queryString'])
		html_content = response.content

	tree = html.fromstring(html_content)

	idx = 2
	while (True):
		#row_xpath='//*[@id="ctl00_SPWebPartManager1_g_54223d45_af2f_49cf_88ed_9e3db1499c51_ctl00_HistoryData1_gridHistoryData_DataGrid1"]/tbody/tr[{row}]/td[{column}]'.format(row=idx,column=7)
		row_xpath='//*[@id="u1st_Skip-links"]/span[1]/a'
		#date is 7.	base madad is 6 and so on
		a = tree.xpath(row_xpath)
		print a
		if not a:
			break
		
		idx = idx + 1

#key is date (2017/3/14). value is weather data dict. csv created columns are date and all data fields
def write_tase_dict_to_csv(tase_data_list,csv_file_name):
    import csv
    fieldnames= tase_data_list[0].keys()

    listWriter = csv.DictWriter(
       open(csv_file_name, 'wb'),
       fieldnames=fieldnames,
       delimiter=',',
       quoting=csv.QUOTE_MINIMAL
    )

    #wrtie the columns names row
    listWriter.writerow(dict(zip(fieldnames,fieldnames)))

    #write all rows
    for day in tase_data_list:
        listWriter.writerow(day)



########
# MAIN #
########

start_date = date(2016, 11, 1)
end_date = date(2017, 11, 7)

#gets data and write it to csv file
TA_125_data = get_TA125_by_dates(start_date,end_date)
#print json.dumps(TA_125_data,indent=4)
write_tase_dict_to_csv(TA_125_data,'tase_test.csv')


