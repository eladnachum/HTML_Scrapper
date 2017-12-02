import requests

def browser_headers_parser(header_str,line_sep):
       #eader_str = "a:b\nc:d"
       return dict(item.split(":") for item in header_str.split(line_sep))




hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
url = "http://www.kolnoapeer.co.il/%D7%9E%D7%A2%D7%A8%D7%9B%D7%AA-%D7%97%D7%95%D7%92%D7%99%D7%9D-%D7%A9%D7%91%D7%95%D7%A2%D7%99/"




res = requests.get(url=url,headers=hdr)
print res.text


