import re
import json
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
		if k not in [':authority',':method',':scheme',':path']:
			out[k]=v
	return out


def get_requests_from_HAR_file (file):
	try:
		requests = json.loads(open(file,'r').read())['log']['entries']
	except:
		print "error. something went wrong extracting the data from HAR file"
		raise
	return requests
