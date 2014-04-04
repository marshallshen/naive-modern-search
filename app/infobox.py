# -*- coding: utf-8 -*-
from __init__ import *
from freebase import FreebaseClient
from models.person import Person
from models.author import Author
from models.actor import Actor
from models.league import League
from models.business_person import BusinessPerson
from models.sports_team import SportsTeam
from models.description import Description

PROPERTIES = {'Person' : ['/people/person'],
              'Author' : ['/book/author'],
              'Actor': ['/film/actor', '/tv/tv_actor'],
              'BusinessPerson' : ['/organization/founder', '/organization/organization_founder', '/business/board_member'],
              'League' : ['/sports/sports_league'],
              'SportsTeam' : ['/sports/sports_team', '/sports/professional_sports_team']}

# excluded these patterns during transforming
EXCLUDED_PROPERTIES = ["/tv/tv_actor/guest_roles"]

API_KEY = "AIzaSyCKQ-u52zqYuBcWxsldypTi0bFEkkPttCE"
class InfoBox(object):
    def __init__(self, query, api_key):
        self.api_key = api_key
        self.query = query
        self.entities = []

    def process(self):
        return self.load(self.transform(self.extract()))

    def extract(self):
        print "extracting...\n"
        result = []
        freebase_client = FreebaseClient(self.api_key)
        search_results = freebase_client.search(self.query)
        if len(search_results['result']) == 0:
            print "No results is found.."
            sys.exit(0)
        for search_result in [search_results['result'][0]]:
            topic_id = search_result['mid']
            raw_topic_response = freebase_client.topic(topic_id)
            result += [raw_topic_response]

        return [result[0]] # TODO: change this to include ALL search response

    def transform(self, raw_topic_response_array):
        print "transforming...\n"
        result = {}

        entities = self.__entity_names__(raw_topic_response_array)
        for entity in entities:
            result[entity] = {}

        # extract model level information
        for raw_topic_response in raw_topic_response_array:
            for entity in entities:
                for stem_pattern in PROPERTIES[entity]:
                    for full_pattern in raw_topic_response['property'].keys():
                        if (len(full_pattern.split(stem_pattern)) > 1) and (full_pattern.split(stem_pattern)[0] == ''): # detect patterns
                            if result[entity].get(stem_pattern) == None:
                                result[entity][stem_pattern] = {}
                            child_pattern = full_pattern.split(stem_pattern)[1].split('/')[1]
                            result[entity][child_pattern] = raw_topic_response['property'][full_pattern]

        # extract description
        result['Description'] = raw_topic_response['property']['/common/topic/description']
        # extract more information for organization
        if result.get('League'):
            if raw_topic_response['property'].get('/organization/organization/slogan'):
                result['League']['slogan'] = raw_topic_response['property']['/organization/organization/slogan']
            if raw_topic_response['property'].get('/common/topic/official_website'):
                result['League']['official_website'] = raw_topic_response['property']['/common/topic/official_website']
        # extract more information for business_person
        if result.get('BusinessPerson'):
            if raw_topic_response['property'].get('/influence/influence_node/influenced'):
                result['BusinessPerson']['influenced'] = raw_topic_response['property']['/influence/influence_node/influenced']

        return result


    def load(self, transformed_response):
        print "loading...\n"

        result = {}
        if transformed_response.get('Person'):
            self.entities += [Person().extract(transformed_response['Person'])]
        if transformed_response.get('Author'):
            self.entities += [Author().extract(transformed_response['Author'])]
        if transformed_response.get('Actor'):
            self.entities += [Actor().extract(transformed_response['Actor'])]
        if transformed_response.get('BusinessPerson'):
            self.entities += [BusinessPerson().extract(transformed_response['BusinessPerson'])]
        if transformed_response.get('League'):
            self.entities += [League().extract(transformed_response['League'])]
        if transformed_response.get('SportsTeam'):
            self.entities += [SportsTeam().extract(transformed_response['SportsTeam'])]
        if transformed_response.get('Description'):
            self.entities += [Description().extract(transformed_response['Description'])]

        header = str(self.query) + "("
        for entity in self.entities:
            if entity.__class__.__name__ != "Description":
                header = header + "  " + str(entity.__class__.__name__)
        header = header +  ")"
        print "----------------------------------"
        print header
        print "----------------------------------"

        for entity in self.entities:
            entity.print_box()
            result[entity.__class__.__name__] = entity

        return result

    def __entity_names__(self, raw_topic_response_array):
        entities = []
        for raw_topic_response in raw_topic_response_array:
            for mapped_property, stem_patterns in PROPERTIES.iteritems():
                for full_pattern in raw_topic_response['property'].keys():
                    for stem_pattern in stem_patterns:
                        if (stem_pattern in full_pattern) and (mapped_property not in entities) and (full_pattern not in EXCLUDED_PROPERTIES) :
                            entities += [mapped_property]
        return entities

def main():
    query =  sys.argv[1]
    info_box = InfoBox(query, API_KEY)
    info_box.process()

if __name__ == "__main__":
    main()
