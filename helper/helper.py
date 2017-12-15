import re
#not using
def convert_qstring_to_dict (str):
    str = str.replace('=','\':\'')
    str = str.replace("&","\',\n\'")
    str = "\'"+str+"\'"
    return str

#not using
def convert_header_to_dict (str):
    re.sub(r'.+: .+\n',r'\'\1\': \'\2\'\n',str)
    print str

#print "{}".format(convert_header_to_dict(str))

#good but stil need to have string with \n separate all lines
#c = dict([[h.partition(':')[0], h.partition(':')[2]] for h in rawheaders.split('\n')])
#print c


def HAR_to_dict (HAR):
	out = {}
	for kv in HAR:
		k = kv['name']
		v = kv['value']
		if v is "null":
			out[k]=None
		else:
			out[k]=v
	return out


def extract_HARS(requests_json):
	requests = []
	required_fields = ['headers','queryString','cookies','postData','method','url']
	entries = requests_json.entries
	for entry in entries:
		for field in required_fields:
			request[field] = entry['request'][field]
		requests.append(request)
	return requests