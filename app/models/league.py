from __init__ import *

class League(object):
    def __init__(self):
        self.sport = None
        self.slogan = None
        self.official_website = None
        self.championship = None
        self.teams = []

    def extract(self, extracted_hash):
        self.sport = extract_value_by_text(extracted_hash, 'sport')
        self.slogan = extract_value_by_text(extracted_hash, 'slogan')
        self.official_website = extract_value_by_text(extracted_hash, 'official_website')
        self.championship = extract_value_by_text(extracted_hash, 'championship')
        self.teams = extract_values_by_property(extracted_hash, 'teams', '/sports/sports_league_participation/team')
        return self

    def print_box(self):
        table = PrettyTable()
        table.add_row(["Sport", self.sport])
        table.add_row(["Slogan", self.slogan])
        table.add_row(["Official Website", self.official_website])
        table.add_row(["championship", self.championship])
        table.add_row(["Teams", "      "])
        for team in self.teams:
            table.add_row(["        ", team])
        table.header = False
        print table