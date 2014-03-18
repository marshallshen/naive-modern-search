from __init__ import *

class Description(object):
    def __init__(self):
        self.text = None

    def extract(self, extracted_hash):
        print extracted_hash
        self.text = extracted_hash['values'][0]['value'].strip()
        return self

    def print_box(self):
        table = PrettyTable()
        table.add_row(['Description'])
        table.add_row([self.text])
        table.header = False
        print table
