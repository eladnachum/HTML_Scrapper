import requests

class costs(object):
    def __init__(self,index_url):
        self.costs_urls = self.get_components_costs_urls(index_url)


    def get_components_costs_urls(self,index_url):
        res = requests.get(index_url)
        print "hi"













