from __init__ import *

class Author(object):
    def __init__(self):
        self.books = []
        self.books_about = []

    def extract(self, extracted_hash):
        self.books = extract_values_by_text(extracted_hash, 'works_written')
        self.books_about = extract_values_by_text(extracted_hash, 'book_editions_published')
        return self

    def print_box(self):
        table = PrettyTable()
        table.add_row(['Books', '    '])
        for book in self.books:
            table.add_row(['    ', book])
        table.add_row(['Books About', '   '])
        for book_about in self.books_about:
            table.add_row(['    ', book_about])
        table.header = False
        table.align = 'l'
        print table