# -*- coding: utf-8 -*-
# API Wrapper for Freebase API
import json
import urllib

BASE_URL = 'https://www.googleapis.com/freebase/v1/'
API_KEY = "AIzaSyCKQ-u52zqYuBcWxsldypTi0bFEkkPttCE"

class FreebaseClient(object):
    def __init__(self, api_key):
        self.api_key = api_key
        self.search_results = []
        self.topic_results = []

    def params(self, query):
        return {'query': query, 'key': self.api_key}

    def search(self, query):
        service_url = BASE_URL + 'search'
        url = service_url + '?' + urllib.urlencode(self.params(query))
        print urllib.urlopen(url).read()
        response = json.loads(urllib.urlopen(url).read())
        for result in response['result']:
            self.search_results.append(result)
            print result['name'] + ' (' + str(result['score']) + ')'

        return self.search_results

    def topic(self, query):
        return null

def main():
    freebase_client = FreebaseClient(API_KEY)
    freebase_client.search("Tolkien")

if __name__ == "__main__":
    main()




