from __init__ import *

class BusinessPerson(object):
    def __init__(self):
        self.board_member = [] # an array of hash
        self.founded = []
        self.leaderships = [] # an array of hash
        self.influenced = []

    def extract(self, extracted_hash):
        self.board_member = extract_nested_values_by_property(extracted_hash, 'organization_board_memberships', ['organization', 'role', 'title', 'from', 'to'])
        self.founded = extract_values_by_text(extracted_hash, 'organizations_founded')
        self.leaderships = extract_nested_values_by_property(extracted_hash, 'leader_of', ['organization', 'role', 'title', 'from', 'to'])
        self.influenced = extract_values_by_text(extracted_hash, 'influenced')
        return self

    def print_box(self):
        table = PrettyTable()
        table.add_row(["Founded", "     "])
        for found in self.founded:
            table.add_row(["     ", found])
        table.add_row(["Influenced", "      "])
        for influence in self.influenced:
            table.add_row(["     ", influence])
        table.header = False
        table.align = 'l'
        print table

        nested_table = PrettyTable()
        nested_table.add_row(["Leadership", "Organization", "Role", "Title", "From", "To"])
        for leadership in self.leaderships:
            nested_table.add_row(["        ", leadership.get("organization"), leadership.get("role"), leadership.get("title"), leadership.get("from"), leadership.get("to")])
        nested_table.add_row(["Board Member", "Organization", "Role", "Title", "From", "To"])
        for member in self.board_member:
            nested_table.add_row(["        ", member.get("organization"), member.get("role"), member.get("title"), member.get("from"), member.get("to")])
        nested_table.header = False
        nested_table.align = 'l'
        print nested_table
