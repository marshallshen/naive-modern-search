from __init__ import *

class Description(object):
    def __init__(self):
        self.text = None

    def extract(self, extracted_hash):
        self.text = extracted_hash['values'][0]['value']
        return self

    def print_box(self):
        print "---------------"
        print "| Description |"
        print "---------------"
        print self.text
