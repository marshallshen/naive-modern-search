from __init__ import *

class Actor(object):
    def __init__(self):
        self.films = []

    def extract(self, extracted_hash):
        self.films = extract_nested_values_by_property(extracted_hash, 'film', ['film', 'character'])
        return self

    def print_box(self):
        table = PrettyTable(["Films", "Character", "Film Name"])
        for film in self.films:
            table.add_row(["    ", film.get('character'), film.get('film')])
        table.align = 'l'
        print table