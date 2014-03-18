# -*- coding: utf-8 -*-
import re

from __init__ import *
from freebase import FreebaseClient

API_KEY = "AIzaSyCKQ-u52zqYuBcWxsldypTi0bFEkkPttCE"
class Magic8Ball(object):
    def __init__(self, raw_query, api_key):
        self.client = FreebaseClient(api_key)
        self.query_detail = self.translate(raw_query)

    def translate(self, raw_query):
        # TODO: regex for pattern matching
        if (len(raw_query.split('Who created ')) == 2) and (len(raw_query.split('Who created ')[1].split('?')) == 2):
            subject = raw_query.split('Who created ')[1].split('?')[0]
        else:
            print "Invalid query, {}...".format(raw_query)
            sys.exit(0)
        return self.__queryable_detail__(subject)

    def answer(self):
        results = []
        for result in self.client.mql(self.query_detail['query'])['result']:
            if result.get(self.query_detail['property']):
                for result_detail in result[self.query_detail['property']]:
                    results += ["{} created {}".format(result['name'], result_detail['a:name'])]

        table = PrettyTable()
        for result in results:
            table.add_row([result])
        table.header = False

        print table
        return results

    def __queryable_detail__(self, subject):
        mid = self.client.search(subject)['result'][0]['mid']
        for type in self.client.topic(mid)['property'].keys():
            if 'organization' in type:
                return {'query': self.__business_person__(subject), 'property': '/organization/organization_founder/organizations_founded'}
        return {'query': self.__author__(subject), 'property': '/book/author/works_written'}

    def __author__(self, name):
        return  [{ "/book/author/works_written": [{
                         "a:name": None, "name~=": name}],
                           "name": None,
                           "type": "/book/author"
                 }]

    def __business_person__(self, name):
        return  [{
                  "/organization/organization_founder/organizations_founded": [{
                    "a:name": None,
                    "name~=": name
                  }],
                "name": None,
                "type": "/organization/organization_founder"
                }]


def main():
    query = sys.argv[1]
    Magic8Ball(query, API_KEY).answer()

if __name__ == "__main__":
    main()

