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
        self.spouses = extract_values_by_property(extracted_hash, 'spouse_s', '/people/marriage/spouse')
        return self

    def print_box(self):
        table = PrettyTable()
        table.add_row(["Birthday", self.birthday])
        table.add_row(["Place Of Birth", self.place_of_birth])
        table.add_row(["Siblings", "      "])
        for sibling in self.siblings:
            table.add_row(["        ", sibling])
        table.add_row(["Spouses", "     "])
        for spouse in self.spouses:
            table.add_row(["        ", spouse])
        table.header = False
        print table