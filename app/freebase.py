# -*- coding: utf-8 -*-
# API Wrapper for Freebase API
from __init__ import *

BASE_URL = 'https://www.googleapis.com/freebase/v1/'
class FreebaseClient(object):
    def __init__(self, api_key):
        self.api_key = api_key

    def search(self, query):
        service_url = BASE_URL + 'search'
        params = {'query': query, 'key': self.api_key}
        url = service_url + '?' + urllib.urlencode(params)

        return json.loads(urllib.urlopen(url).read())

    def topic(self, topic_id):
        service_url = BASE_URL + 'topic' + topic_id
        params = {'key': self.api_key}
        url = service_url + '?' + urllib.urlencode(params)

        return json.loads(urllib.urlopen(url).read())

    def mql(self, query):
        service_url = BASE_URL + 'mqlread'
        params = {'query': json.dumps(query), 'key': self.api_key}
        url = service_url + '?' + urllib.urlencode(params)

        return json.loads(urllib.urlopen(url).read())