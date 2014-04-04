from __init__ import *

class SportsTeam(object):
    def __init__(self):
        self.arena = None
        self.sport = None
        self.founded = None
        self.location = None
        self.championships = []
        self.leagues = []
        self.players_roster = []
        self.coaches = []

    def extract(self, extracted_hash):
        self.arena = extract_value_by_text(extracted_hash, 'arena_stadium')
        self.founded = extract_value_by_text(extracted_hash, 'founded')
        self.sport = extract_value_by_text(extracted_hash, 'sport')
        self.leagues = extract_values_by_property(extracted_hash, 'league', '/sports/sports_league_participation/league')
        self.location = extract_value_by_text(extracted_hash, 'location')
        self.championships = extract_values_by_text(extracted_hash, 'championships')
        self.players_roster = extract_nested_values_by_property(extracted_hash, 'roster', ['player', 'position', 'from', 'to'])
        self.coaches = extract_nested_values_by_property(extracted_hash, 'coaches', ['coach', 'position', 'from', 'to'])
        return self

    def print_box(self):
        table = PrettyTable()
        table.add_row(["Sport", "       "])
        table.add_row(["    ", self.sport])
        table.add_row(["Arena", "       "])
        table.add_row(["    ", self.arena])
        table.add_row(["Founded", "       "])
        table.add_row(["    ", self.founded])
        table.add_row(["Location", "       "])
        table.add_row(["    ", self.location])
        table.add_row(["Championships", "       "])
        for championship in self.championships:
            table.add_row(["    ", championship])
        table.add_row(["Leagues", "       "])
        for league in self.leagues:
            table.add_row(["    ", league])
        table.header = False
        table.align = 'l'
        print table

        nested_table = PrettyTable()
        if len(self.players_roster) > 0:
            nested_table.add_row(["Roster", "Player", "Position", "From", "To"])
            for roster in self.players_roster:
                nested_table.add_row(["      ", roster.get("player"), roster.get("position"), roster.get("from"), roster.get("to")])

        if len(self.coaches) > 0:
            nested_table.add_row(["     ", "    ", "    ", "    ", "    "])
            nested_table.add_row(["Coach", "Name", "Position", "From", "To"])
            for coach in self.coaches:
                nested_table.add_row(["     ", coach.get("coach"), coach.get("position"), coach.get("from"), coach.get("to")])

        if (len(self.players_roster) > 0 or len(self.coaches) > 0):
            nested_table.header = False
            nested_table.align = 'l'
            print nested_table