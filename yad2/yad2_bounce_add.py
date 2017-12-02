import urllib2
import requests
from lxml import html
import json


#https://my.yad2.co.il/newOrder/index.php?action=updateBounceListing&CatID=3&SubCatID=0&OrderID=33431754
url = "https://my.yad2.co.il"
method = "POST"
endpoint = "/newOrder/index.php?action=updateBounceListing&CatID=3&SubCatID=0&OrderID=33431754"

#no need...
query_string = 'action=updateBounceListing&CatID=3&SubCatID=0&OrderID=33431754'

hdr = {
'Host': 'my.yad2.co.il',
'Connection': 'keep-alive',
'Content-Length': '203',
'Accept': 'application/json, text/javascript, */*; q=0.01',
'Origin': 'https://my.yad2.co.il',
'X-Requested-With': 'XMLHttpRequest',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-16',
'Referer': 'https://my.yad2.co.il/newOrder/index.php?action=personalAreaViewDetails&CatID=3&SubCatID=0&OrderID=33431754',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'en-US,en;q=0.8,he;q=0.6',
'Cookie': 'historyprimaryarea=hamerkaz_area; historysecondaryarea=tel_aviv_east; __za_cd_19762211=%7B%22visits%22%3A%22%5B1501666711%2C1500447739%2C1500185000%5D%22%7D; SaveSearch_CustID=hic7847586474; searchB144FromYad2=2_C_1800; favorites_userid=idi2559750402; _ga=GA1.3.4485375.1498981918; _gid=GA1.3.1153597695.1502976989; _dc_gtm_UA-708051-1=1; PHPSESSID=5719052360c135d057857987ceb63bc8; uci=bbb8c9762414b739b879e1b32dd537ac; id=6c4ca2733ee223626dad02334eb9ac7f__20170815233057__1ea5d2152fb87593786139e94b7a5fe1; sid=5719052360c135d057857987ceb63bc8; login=201708171636; USERNAME=seladnac%40gmail.com; USER_NAME=seladnac; uType_Car=0; uType_Nadlan=0; uType_yad2=0; myyad2=50331658.20480.0000; TS01360dcb=01cdef7ca275cbc6fe375ded3fe96d6c6c7eaef439afcfe814a8a25c6974d9fe311ddc7fb7d3fff4308446ea081595af9b80dea80688fe4cba3eb918d2960366e366f249aab8feae39b194934c903d8f4a3d25ab4be76a603b3822db2d70d9c44c177979ff439c52268edf7872655df68940f7f611fd9b05b1358bc6948b562585bb965f7f264be6973cdf300af7d33fb50d58eddb0bf794d883d2bfdb38805e104894e7ce0bc8ab618382c62eedf9d25e3894a56ced13e6fd105aff879347b6be9200fee9572163d34765741977e5c4bfeb27f423e278c23168f1bdb435c60ff73b809550b1c01b2cbbd664a29d586b1cee20c9461171358e9e477a1ce8eadcfa962e4250f92644f37beb9af28246bf668970cb5f0aa0bb3a58ffe8ca90305e179033adfeadb4e70eb3af1fc1280211cfbd43544a36af838862d402fbdd6a072faab3ae85e9266c8df54e9d8249a95ff5ef8804c8ff124834df38adf2814a7c44470c1381d05a3dbeb5177ec02cc16890656d39cf60f59f796bbf8c48a496dc114f7928ee; TS01da816a=01cdef7ca20c0755c85d35115dddb1eb0e40bf1775f9597fb491e3d2d8cc0f72f9b4dbebefb812d2f334694d53d1a407501219a741b0d6aec40bb90cc92e617214f7d1be69; _ga=GA1.4.4485375.1498981918; _gid=GA1.4.1153597695.1502976989; _gat_UA-708051-1=1'
}
data_form = {
'isTrader':'0',
'OrderID':'33431754',
'RecordID':'13712484',
'CatID':'3',
'SubCatID':'0',
'state':'2',
'StatusID':'1',
'Image1':'o3_0_1_174885_20170815230848.jpg',
'Image2':'o3_0_2_179075_20170815230852.jpg',
'Image3':'o3_0_3_176215_20170815230858.jpg'
}


res = requests.post(url=url+endpoint,data=data_form)
#str =  repr(res.text)
outfile = open('scrapper_response.html', 'w')
outfile.write(res.content)
outfile.close()