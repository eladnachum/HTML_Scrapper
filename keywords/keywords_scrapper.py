import urllib2
import requests
from lxml import html
import json
from helper import HAR_to_dict
import sys


def remove_keys(the_dict,keys):
  for key in keys:
    del the_dict[key]




hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

hdr2 = {
	'accept':'*/*',
	'accept-encoding':'gzip, deflate, br',
	'accept-language':'en-US,en;q=0.8,he;q=0.6',
	'content-length':'3813',
	'content-type':'text/x-gwt-rpc; charset=UTF-8',
	'cookie':'_pgar=https%3A%2F%2Fadwords.google.com%2Fum%2FGetStarted%2FHome%3F__u%3D8366573661%26__c%3D6519561002%26authuser%3D0; CONSENT=YES+IL.en+20160815-07-0; 1P_JAR=2017-11-16-8; NID=117=CFsGNh7AFJ99eq75zSqCRHpocMEpFAnhgkD0WAHEj0JxG59-XRgO2FLXFqG9Sear3YuFQFHzwWcGz6pdamjrsjWh_1AGvZfElHajny51dIznZdvIeMMbLCjQsbxjKZdc26cgAyKtWfM5UyVg4o1FuI-z4FjWGm4xoGXQJUdcMCtWcBWeybgEQXfZ8EDFZhLWlpW9tQYvJXk80ABFoQH7_U95e3Xu43BD8WczEODXNCNcZA_YMOAWGQzHLxBZQNTzk5upcO0tSWskd8JsrXG3dOQup6lKj_ws; gap%3AUA-37177323-1%3A18558082978=%7B%22mobile%22%3A%22%2B18553527879%22%2C%22display%22%3A%22(855)%20352-7879%22%2C%22expires%22%3A1510914099%7D; HSID=ATDQqKMj6V3tx2dJn; SSID=AOnj4jYBapzt8yfrQ; APISID=O6iPuo5ioMd1aqRV/A5KD4DIc-sHph9bKg; SAPISID=lnuk_q_2iZkbcHrP/Ar_Eq4P_gopFdq2Ar; SAG=awWwtHtQwHvNy8b8JM9HzMAqaSfQcYW8-hwr7MrkhODAliIQO3Geg8G3ajce9T_vL7oREA.; adwordsReferralSource=sourceid=emp&subid=ww-ww-et-g-aw-a-tools-awhp!o2&clickid=sn-6r-og-il-11172017; S=adwords-usermgmt=f_k304DjiHhHTQe1LjB3Q8QU9TIRpBFZ:billing-ui-v3=C1jsysJWfrXzgN9-9DoeUtxQqN3e5wVC:billing-ui-v3-efe=C1jsysJWfrXzgN9-9DoeUtxQqN3e5wVC; A=AIxWtxRjxKqN0UNZ0ZO2dVjntf-dlyIlRtcKYIgyI8kuiWh3f601lV77aD58Q0-rlpxV2bvSfkmq-2eKx1SshkrCssfxN93iNpPfPpyz7cbH0V0G1Egz0_7nD6hjNj3uElgONzh97qcuTTwHOupLwwcwYeLAZs9C6CrpGb-cz7Tpllx_RBj-o6yV-a8D7vxHu6UcLUh5dqwm; AdsUserLocale=en_US; SID=awWwtHnhtIZLsxhekk3ktFDnHGS3Qqa8sEwGJHZkJHvqMMpgaKGb3-DeICXo-9cVPWNfHw.; _gat_UA-37177323-1=1; SIDCC=AE4kn7_BRBiYBxE7ufTsBVpMGtJhPdyN4xkxsoNWdKSgLJNf2fLjM9-Frlg-hlSy17VBvfA2cx6M39RY6QA; _ga=GA1.3.1574563537.1510908700; _gid=GA1.3.1683483841.1510908700',
	'origin':'https://adwords.google.com',
	'referer':'https://adwords.google.com/um/GetStarted/Home?__u=8366573661&__c=6519561002&authuser=0',
	'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
	'x-chrome-uma-enabled':'1',
	'x-client-data':'CJK2yQEIpbbJAQjEtskBCPqcygEIqZ3KAQjSncoBCKijygE=',
	'x-gwt-module-base':'https://adwords.google.com/um/GetStarted/com.google.ads.apps.usermgmt.getstarted.client.main.Module/',
	'x-gwt-permutation':'CE05809FCF765752ADFEF2124C64CD4B'
}

headers1 =  [
            {
              "name": "origin",
              "value": "https://adwords.google.com"
            },
            {
              "name": "accept-encoding",
              "value": "gzip, deflate, br"
            },
            {
              "name": "accept-language",
              "value": "en-US,en;q=0.8,he;q=0.6"
            },
            {
              "name": "x-gwt-permutation",
              "value": "CE05809FCF765752ADFEF2124C64CD4B"
            },
            {
              "name": "x-chrome-uma-enabled",
              "value": "1"
            },
            {
              "name": "x-gwt-module-base",
              "value": "https://adwords.google.com/um/GetStarted/com.google.ads.apps.usermgmt.getstarted.client.main.Module/"
            },
            {
              "name": "cookie",
              "value": "CONSENT=YES+IL.en+20160815-07-0; 1P_JAR=2017-11-16-8; gap%3AUA-37177323-1%3A18558082978=%7B%22mobile%22%3A%22%2B18553527879%22%2C%22display%22%3A%22(855)%20352-7879%22%2C%22expires%22%3A1510914099%7D; HSID=ATDQqKMj6V3tx2dJn; SSID=AOnj4jYBapzt8yfrQ; APISID=O6iPuo5ioMd1aqRV/A5KD4DIc-sHph9bKg; SAPISID=lnuk_q_2iZkbcHrP/Ar_Eq4P_gopFdq2Ar; SAG=awWwtHtQwHvNy8b8JM9HzMAqaSfQcYW8-hwr7MrkhODAliIQO3Geg8G3ajce9T_vL7oREA.; adwordsReferralSource=sourceid=emp&subid=ww-ww-et-g-aw-a-tools-awhp!o2&clickid=sn-6r-og-il-11172017; A=AIxWtxRjxKqN0UNZ0ZO2dVjntf-dlyIlRtcKYIgyI8kuiWh3f601lV77aD58Q0-rlpxV2bvSfkmq-2eKx1SshkrCssfxN93iNpPfPpyz7cbH0V0G1Egz0_7nD6hjNj3uElgONzh97qcuTTwHOupLwwcwYeLAZs9C6CrpGb-cz7Tpllx_RBj-o6yV-a8D7vxHu6UcLUh5dqwm; AdsUserLocale=en_US; SID=awWwtHnhtIZLsxhekk3ktFDnHGS3Qqa8sEwGJHZkJHvqMMpgaKGb3-DeICXo-9cVPWNfHw.; NID=117=I-ZcVgfMmtlsD4d99l4XQjajRJLPV9veNtamKrPmT05NXlFJh7BvyPY2CRYr2mZbEzKvzdzlr_qJe8bcrfYhcUNSn9f1rYQMtEYm2HDMnRMA_YOe6kncNH4GjpvL7QPU2eqG428ioECAsuFRN_3cS0uOOkBBSHFQWok-uSOG8lPirJOBB3fH7jRm0bB2ilsW-jQdT8AEt3r83RhYVYRUcVLY1yTkPvxG1mbRPhVBgOD94NaJefu5Grp2ReZogzGaxBrccLzq2YQ45hIe0ivwySdVAEgGsEGB; _gat_UA-37177323-1=1; S=adwords-usermgmt=XQw93ZwEBOE5FnA0ufVSLvD7-aEDWKDB:billing-ui-v3=ozH8lv-V270PaYwi8aLTS7XwYurC5y4h:billing-ui-v3-efe=ozH8lv-V270PaYwi8aLTS7XwYurC5y4h; SIDCC=AE4kn786sL3Ndw1_KmLBvYvTxrxyhNtH4xker1UnuNcs6SxGvMcMMtHXcZTzf-JEPNV5nuxwC9d8Q1yUBgc; _ga=GA1.3.1574563537.1510908700; _gid=GA1.3.1683483841.1510908700"
            },
            {
              "name": "x-client-data",
              "value": "CJK2yQEIpbbJAQjEtskBCPqcygEIqZ3KAQjSncoBCKijygE="
            },
            {
              "name": "content-length",
              "value": "3813"
            },
            {
              "name": "user-agent",
              "value": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
            },
            {
              "name": "content-type",
              "value": "text/x-gwt-rpc; charset=UTF-8"
            },
            {
              "name": "accept",
              "value": "*/*"
            },
            {
              "name": "referer",
              "value": "https://adwords.google.com/um/GetStarted/Home?__u=8366573661&__c=6519561002&authuser=0"
            }
          ]


data1 = "7|0|76|https://adwords.google.com/um/GetStarted/com.google.ads.apps.usermgmt.getstarted.client.main.Module/|22D5B3FA3CEBB378F43793C10A1E70DB|com.google.ads.api.gwt.rpc.client.BatchedInvocationService|invoke|com.google.ads.api.gwt.rpc.client.BatchedInvocationRequest/2983766987|com.google.ads.apps.common.shared.header.BatchRequestHeaderImpl/2595329959|java.util.HashMap/1797211028|com.google.ads.apps.common.shared.header.ApiHeaderType/3992732687|com.google.ads.apps.common.shared.header.BatchAdsApiRequestHeaderInfo/1561664655|com.google.ads.api.modules.request.headers.GrubbyHeader$ChangeIdMode/272930539|com.google.ads.apps.common.usagetracking.server.UsageTrackingService.logImpression|rGRQNhESwLJgUXz8hBjKCfxyUFw:1510910684674|java.util.ArrayList/4159755760|com.google.ads.apps.common.usagetracking.shared.UsageTrackingServiceGwt$ImpressionRequest/3960782202|com.google.ads.apps.common.shared.header.SingleAdsApiRequestHeader/4098801396|com.google.ads.apps.common.shared.header.ClientCacheHint/2402802613|com.google.ads.apps.common.shared.header.ServerCacheHint/3129959624|java.lang.Boolean/476441737|com.google.ads.api.modules.request.headers.ApiVersion/450371163|com.google.ads.api.modules.request.headers.GrubbyHeader$CustomerIdMode/45453300|com.google.ads.api.modules.request.headers.GrubbyHeader$DatabaseReadMode/1150601902|com.google.common.collect.RegularImmutableList/440499227|com.google.ads.common.logging.MetricEntries$ImpressionEntry/454587110|[Lcom.google.ads.common.logging.ApexExperimentMetrics;/1267822276|com.google.ads.common.logging.ApexExperimentMetrics/1204991806|TREATMENT|java.lang.String/2004016611|AWSM|AWN_INTERNALOPS|MCC|NOTIFICATIONS|UM|ADWORDS_NEXT_BILLING||CUES|ADWORDS_NEXT_MCC|ADWORDS_NEXT_INTERNALOPS|ADWORDS_NEXT_ACCESS_TO_ALL|TREATMENT_SIGNUP_FLOW_CLICKS_WITH_BADGES|CM|CM_GROWTH_MOBILE_PROMO|CT|PRIME|AWN_PRIME|AWN_CM|ADWORDS_NEXT|ADWORDS_NEXT_NEW_CUSTOMERS|KP|ADWORDS_NEXT_KEYWORD_PLANNER|https://adwords.google.com/um/GetStarted/Home?__u=8366573661&__c=6519561002&authuser=0#oc|[Lcom.google.ads.common.logging.ExperimentMetrics;/2152658160|com.google.ads.common.logging.ExperimentMetrics/1213839764|enable-call-consent|com.google.common.collect.RegularImmutableMap/1085455152|remove-progress-bar|enable-appstore|orinoco-megablox|get-started-w-logo|show-estimated-reach-panel|expanded-text-ad|youtube-linked-accounts|show-top-ad-preview|enable-goldmine-auto-expand|u2-migration|default-opt-in|billing-all-countries|enable-auto-expand|rewire-guided-orinoco-billing-for-budgets-in-ads|mobile-compatible-orinoco|policy-certificate-expiration|target-cpa-suggestion|electrum-account-linking-ui|[Ljava.lang.String;/2600011424|Orinoco.oc.keywords-editor-keywords-input-focused|oc.keywords-editor-keywords-input-focused|com.google.ads.apps.common.uimode.shared.UiMode/4208379950|1|2|3|4|1|5|5|6|quRMuCHZo|45|7|1|8|0|9|A|10|2|GEmJsq|Hyr8hd|11|12|13|1|14|15|16|0|0|17|13|0|18|0|18|1|0|0|19|6|0|A|0|0|0|0|0|0|0|0|20|0|21|1|0|0|0|0|0|1|1|0|0|0|0|0|0|0|0|0|0|0|0|22|0|0|0|0|7|0|0|0|0|23|24|8|25|0|1|26|22|5|27|28|27|29|27|30|27|31|27|32|33|0|252|34|FUlReeu8O|25|0|1|26|22|3|-24|27|35|-28|36|0|252|34|FWguhina5|25|0|1|26|22|3|-24|-31|-28|37|0|252|34|FW9cs8QQc|25|0|1|26|22|3|-24|-31|-28|38|0|749|34|FW9cs8QQc|25|0|1|39|22|2|27|40|-28|41|0|340|34|FV4L2$Qzk|25|0|0|34|22|9|-24|-31|-28|27|42|27|43|27|44|-25|27|45|-38|46|0|252|34|FWzMJiJ_3|25|0|1|26|22|3|-24|-31|-28|47|0|252|34|FWzhhJjZK|25|0|0|34|22|3|-24|-28|27|48|49|0|252|34|FW1uiRGFm|50|0|51|19|52|53|54|0|1|1|1|52|55|-52|1|1|1|52|56|-52|1|1|1|52|57|-52|1|1|1|52|58|-52|1|1|1|52|59|-52|1|1|1|52|60|-52|1|1|1|52|61|-52|1|1|0|52|62|-52|1|1|1|52|63|-52|1|1|1|52|64|-52|1|1|1|52|65|-52|1|1|1|52|66|-52|1|1|1|52|67|-52|1|1|1|52|68|-52|1|1|1|52|69|-52|1|1|1|52|70|-52|1|1|1|52|71|-52|1|1|1|52|72|-52|1|1|1|V_JTowC|73|0|-1|74|73|1|75|76|0|"

url1 = "https://adwords.google.com/um/GetStarted/g?authuser=0&__u=8366573661&__c=6519561002"

# response = requests.post(url1,headers=HAR_to_dict(headers1),data=data1)
# print "RESPOSNE 1:"
# print json.dumps(response.content,indent=4)


requests_dict = json.load(open("HAR_req.json",'r'))
my_requests = requests_dict['log']['entries']
responses = []

for request in my_requests:
  url = request['request']['url']
  headers = HAR_to_dict(request['request']['headers'])
  method = request['request']['method']
  if method == "POST":
    data = request['request']['postData']
    responses.append(requests.post(url=url,headers=headers,data=data))
  if method == "GET":
    responses.append(requests.get(url=url,headers=headers))

for response in responses:
  print "RESPONSE:"
  print response.content





