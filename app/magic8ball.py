# -*- coding: utf-8 -*-
import re

from __init__ import *
from freebase import FreebaseClient

API_KEY = "AIzaSyCKQ-u52zqYuBcWxsldypTi0bFEkkPttCE"
class Magic8Ball(object):
    def __init__(self, raw_query, api_key):
        self.client = FreebaseClient(api_key)
        self.raw_query = raw_query
        self.query_details = self.translate(raw_query)

    def translate(self, raw_query):
        # TODO: regex for pattern matching
        if (len(raw_query.split('Who created ')) == 2) and (len(raw_query.split('Who created ')[1].split('?')) == 2):
            subject = raw_query.split('Who created ')[1].split('?')[0]
        else:
            print "Invalid query, {}...".format(raw_query)
            sys.exit(0)
        return [{'query': self.__author__(subject), 'property': '/book/author/works_written', 'type': 'Author'},
                {'query': self.__business_person__(subject), 'property': '/organization/organization_founder/organizations_founded', 'type': 'BusinessPerson'}]

    def answer(self):
        table = PrettyTable()

        print "------------------------------------------"
        print self.raw_query
        print "------------------------------------------"

        # Beginning compose results
        results_hash = {}
        for query_detail in self.query_details:
            results_hash[query_detail['type']] = {}
            for result in self.client.mql(query_detail['query'])['result']:
                if result.get(query_detail['property']):
                    for result_detail in result[query_detail['property']]:
                        results_hash[query_detail['type']][result['name']] = result_detail['a:name']

        print results_hash

        compact_results_hash = {}
        for type, answers_by_type in results_hash.iteritems():
            compact_results_hash_by_type = {}
            for key, value in answers_by_type.iteritems():
                if compact_results_hash_by_type.get(key):
                    compact_results_hash[key] += [value]
                else:
                    compact_results_hash_by_type[key] = [value]
            compact_results_hash[type] = compact_results_hash_by_type
        # Ending compose results

        # Beginning printing results
        for type, answers_by_type in compact_results_hash.iteritems():
            for creator, creations in answers_by_type.iteritems():
                table.add_row([creator, 'AS', 'Creation'])
                table.add_row(['    ', type, '/n '.join(creations)])
        # Ending printing results

        table.header = False
        table.align = 'l'
        print table

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

