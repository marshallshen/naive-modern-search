from __init__ import *

class Person(object):
    def __init__(self):
        self.birthday = None
        self.place_of_birth = None
        self.siblings = []
        self.spouses = []

    def extract(self, extracted_hash):
        self.birthday = extract_value_by_text(extracted_hash, 'date_of_birth')
        self.place_of_birth = extract_value_by_text(extracted_hash, 'place_of_birth')
        self.siblings = extract_values_by_property(extracted_hash, 'sibling_s', '/people/sibling_relationship/sibling')
        if extracted_hash.get('spouse_s'):
            self.spouses = self.composite_values_by_property(extracted_hash['spouse_s'])

        return self

    def composite_values_by_property(self, spouses_hash):
        results = []
        for value in spouses_hash['values']:
            # optional values
            location = None
            married_from = None
            married_to = None

            spouse = value['property']['/people/marriage/spouse']['values'][0]['text']
            if value['property'].get('/people/marriage/location_of_ceremony') and len(value['property']['/people/marriage/location_of_ceremony'].get('values')) > 0:
                location = value['property']['/people/marriage/location_of_ceremony']['values'][0]['text']
            if value['property'].get('/people/marriage/from') and len(value['property']['/people/marriage/from'].get('values')) > 0:
                married_from = value['property']['/people/marriage/from']['values'][0]['text']
            if value['property'].get('/people/marriage/to') and len(value['property']['/people/marriage/to'].get('values')) > 0:
                married_to = value['property']['/people/marriage/to']['values'][0]['text']

            result = str(spouse)
            if location:
                result = result + " @ " + location
            if married_from:
                result = result + "  " + married_from
            if married_to:
                result = result + " ~ " + married_to

            results += [result]

        return results


    def print_box(self):
        table = PrettyTable()
        table.add_row(["Birthday", self.birthday])
        table.add_row(["Place Of Birth", self.place_of_birth])
        if len(self.spouses) > 0:
            table.add_row(["Spouses", "     "])
            for spouse in self.spouses:
                table.add_row(["        ", spouse])
        if len(self.siblings) > 0:
            table.add_row(["Siblings", "      "])
            for sibling in self.siblings:
                table.add_row(["        ", sibling])
        table.align = 'l'
        table.header = False
        print table