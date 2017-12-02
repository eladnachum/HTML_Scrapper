import urllib2
import requests
from lxml import html
import json

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

hdr2 = {
    'Host': 'www.amazon.com',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Referer': 'https://www.amazon.com/s/ref=nb_sb_ss_c_1_6?url=search-alias%3Daps&field-keywords=4tb+external+hard+drive&sprefix=4tb+ex%2Caps%2C314&crid=3UWB6F0D634O8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.8,he;q=0.6',
    'Cookie': 'x-wl-uid=19m4kzOtpnWJqS2O/cSAzVVYEDb+PjXmL/Q0q7Y1Xt6ZanUa0jur6rfSsWMdJZC+2cwMUBfDq0Uo=; session-token=sKGxN453BBvd8V0vBCkg/8E+JbzPH89R5U8w0eQLZwiCg9ogyIPgLaD4XaDbLD5wl9aEL+7kIH02CcKotn9WwhzL/anEAm6UTFuHQpucksVLxG/8gM3IV3DX2khCJ1UyWGHkGTdQ56/J9nac/PbaLXNG9mRIzTyK5fDQJ5QpIVfq4Z3KbTJnkNRpzzjJxzQ3qak1rYk5MfN5+TTRpaGLLegEAM1Ml7/UaUb9scZ2pE4ywnrVdC8q+Wbwg4zaDsHK; aws-target-static-id=1487489471842-40657; _mkto_trk=id:112-TZM-766&token:_mch-aws.amazon.com-1487489473275-10075; s_vn=1505721114959%26vn%3D21; aws-session-id-time=2082787201l; aws-session-id=146-9091906-0951346; __utmz=194891197.1497877663.8.5.utmccn=(referral)|utmcsr=portal.aws.amazon.com|utmcct=/billing/signup|utmcmd=referral; aws-ubid-main=163-3753862-2680314; aws-session-token="4g5p8YPaFX2I7/NhmZleZJ3SGyVmO4fn2PrM1vj9G5fEmASCw3BwuzHoFhQgCN7dZDuO5PATUF1NzTT89S/Ou70w4OFhsypscpt9vP0Nti8RSUYuXdDVBWhnXIzUK9cOdceOhcOCDzzcANI3xojRp4zPWjfhaVcoHdiqa1yZXP67DThlQnyPr2AgnlwAXIz1djTWyKPtulsi1Fl/57x1qXFSl5KcraHV53ZiMgrIs+Y="; aws-x-main="orW6WIVyWPj0weqAJOu4mXwtWkROu?rCD0QnQal9Uc7JBYY@rbboOLrGRH@UejFI"; aws-at-main=Atza|IwEBIEwKRWH6O3HnkQXaVDxARdNElC65NsSk36FPglK72RTWdNiGhijaQERi-vFbkZQNxlv327KvGCtVRS8U83S1SlOp86WUzyJyRWJ4Y_bGDJyTxsNTAAfRf_lbs3sEMxW1F0p8Sg0LhURrqJg3lvJs3E5tQbQjafxUSEtBR8rMpZI5IeNRQ17ZzXz64MLSoH7YnMbPJLn9UQhdtYNXlDtVHYGDHHWtFhQRaf5bPql8eyGL3jHv1o6RHppe3GinBbWwFzESjohH03bwBiDyoY4rSApJs52vBDOIeWdLNs_ViWlsNxysggrbMOFotycpXGOsg6wzyJe1d5IOzxmsAwcKfr2yDBXrnQcRlQlCRpwHl3rSemgx4BeJQJzxizGI1aDUFhJSsF-rE0t6sO4nLyDvIXKA_m4YUqN5pYCXRLnUJsePUQ; aws-userInfo=%7B%22arn%22%3A%22arn%3Aaws%3Aiam%3A%3A314852337498%3Aroot%22%2C%22alias%22%3A%22%22%2C%22username%22%3A%22elad%22%2C%22keybase%22%3A%222cmrUtkYoRwXTMwLO3YPitod%2F%2BZN89ParWppYo62nog%5Cu003d%22%2C%22issuer%22%3A%22https%3A%2F%2Fwww.amazon.com%2Fap%2Fsignin%22%7D; __utmv=194891197.%22orW6WIVyWPj0weqAJOu4mXwtWkROu%3FrCD0QnQal9Uc7JBYY%40rbboOLrGRH%40UejFI%22; __utma=194891197.1024196377.1488096123.1497877663.1497877866.9; aws-business-metrics-last-visit=1497878097966; aws-target-visitor-id=1487489471847-859317.26_22; aws-target-data=%7B%22support%22%3A%221%22%7D; s_fid=74E413CC94469FC7-07A4FCB56AEB34A3; s_dslv=1497878810915; s_nr=1497878810917-Repeat; regStatus=registered; skin=noskin; JSESSIONID=D02CC213F50D6EEABA514B1A471F4BDB; csm-hit=99Q0V1AT3TBYWAWT51EB+b-7CYHKZSGJ9JMN0Q42H4M|1502778988550; ubid-main=157-8202911-6880618; session-id-time=2082787201l; session-id=153-7549086-9875251'
}

hdr3 = {
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate, br',
'Accept-Language':'en-US,en;q=0.8,he;q=0.6',
'Connection':'keep-alive',
'Cookie':'x-wl-uid=19m4kzOtpnWJqS2O/cSAzVVYEDb+PjXmL/Q0q7Y1Xt6ZanUa0jur6rfSsWMdJZC+2cwMUBfDq0Uo=; session-token=sKGxN453BBvd8V0vBCkg/8E+JbzPH89R5U8w0eQLZwiCg9ogyIPgLaD4XaDbLD5wl9aEL+7kIH02CcKotn9WwhzL/anEAm6UTFuHQpucksVLxG/8gM3IV3DX2khCJ1UyWGHkGTdQ56/J9nac/PbaLXNG9mRIzTyK5fDQJ5QpIVfq4Z3KbTJnkNRpzzjJxzQ3qak1rYk5MfN5+TTRpaGLLegEAM1Ml7/UaUb9scZ2pE4ywnrVdC8q+Wbwg4zaDsHK; aws-target-static-id=1487489471842-40657; _mkto_trk=id:112-TZM-766&token:_mch-aws.amazon.com-1487489473275-10075; s_vn=1505721114959%26vn%3D21; aws-session-id-time=2082787201l; aws-session-id=146-9091906-0951346; __utmz=194891197.1497877663.8.5.utmccn=(referral)|utmcsr=portal.aws.amazon.com|utmcct=/billing/signup|utmcmd=referral; aws-ubid-main=163-3753862-2680314; aws-session-token="4g5p8YPaFX2I7/NhmZleZJ3SGyVmO4fn2PrM1vj9G5fEmASCw3BwuzHoFhQgCN7dZDuO5PATUF1NzTT89S/Ou70w4OFhsypscpt9vP0Nti8RSUYuXdDVBWhnXIzUK9cOdceOhcOCDzzcANI3xojRp4zPWjfhaVcoHdiqa1yZXP67DThlQnyPr2AgnlwAXIz1djTWyKPtulsi1Fl/57x1qXFSl5KcraHV53ZiMgrIs+Y="; aws-x-main="orW6WIVyWPj0weqAJOu4mXwtWkROu?rCD0QnQal9Uc7JBYY@rbboOLrGRH@UejFI"; aws-at-main=Atza|IwEBIEwKRWH6O3HnkQXaVDxARdNElC65NsSk36FPglK72RTWdNiGhijaQERi-vFbkZQNxlv327KvGCtVRS8U83S1SlOp86WUzyJyRWJ4Y_bGDJyTxsNTAAfRf_lbs3sEMxW1F0p8Sg0LhURrqJg3lvJs3E5tQbQjafxUSEtBR8rMpZI5IeNRQ17ZzXz64MLSoH7YnMbPJLn9UQhdtYNXlDtVHYGDHHWtFhQRaf5bPql8eyGL3jHv1o6RHppe3GinBbWwFzESjohH03bwBiDyoY4rSApJs52vBDOIeWdLNs_ViWlsNxysggrbMOFotycpXGOsg6wzyJe1d5IOzxmsAwcKfr2yDBXrnQcRlQlCRpwHl3rSemgx4BeJQJzxizGI1aDUFhJSsF-rE0t6sO4nLyDvIXKA_m4YUqN5pYCXRLnUJsePUQ; aws-userInfo=%7B%22arn%22%3A%22arn%3Aaws%3Aiam%3A%3A314852337498%3Aroot%22%2C%22alias%22%3A%22%22%2C%22username%22%3A%22elad%22%2C%22keybase%22%3A%222cmrUtkYoRwXTMwLO3YPitod%2F%2BZN89ParWppYo62nog%5Cu003d%22%2C%22issuer%22%3A%22https%3A%2F%2Fwww.amazon.com%2Fap%2Fsignin%22%7D; __utmv=194891197.%22orW6WIVyWPj0weqAJOu4mXwtWkROu%3FrCD0QnQal9Uc7JBYY%40rbboOLrGRH%40UejFI%22; __utma=194891197.1024196377.1488096123.1497877663.1497877866.9; aws-business-metrics-last-visit=1497878097966; aws-target-visitor-id=1487489471847-859317.26_22; aws-target-data=%7B%22support%22%3A%221%22%7D; s_fid=74E413CC94469FC7-07A4FCB56AEB34A3; s_dslv=1497878810915; s_nr=1497878810917-Repeat; regStatus=registered; skin=noskin; JSESSIONID=D02CC213F50D6EEABA514B1A471F4BDB; ubid-main=157-8202911-6880618; session-id-time=2082787201l; session-id=153-7549086-9875251; csm-hit=99Q0V1AT3TBYWAWT51EB+s-K8MWHSKBEEPTV5FJGW96|1502779737014',
'Host':'www.amazon.com',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
}

site_url = "https://www.amazon.com/Fantom-Drives-Aluminum-External-GF3B4000EU/dp/B00CR9Q6MI/ref=sr_1_2?s=pc&ie=UTF8&qid=1502780601&sr=1-2-spons&keywords=4tb+external+hard+drive&psc=1"

#respone is an object. response.text and response.content will have the data returned (usually the html)
response = requests.get(site_url,headers=hdr2)

#Write the html into a file (not neccessary)
str =  repr(response.text)
outfile = open('scrapper_response.html', 'w')
outfile.write(str)
outfile.close()
