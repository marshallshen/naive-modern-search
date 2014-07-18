import web
from __init__ import *
from app.freebase import FreebaseClient
from app.infobox import InfoBox
from app.magic8ball import Magic8Ball

urls = (
  '/search', 'Index'
)

app = web.application(urls, globals())

render = web.template.render('templates/', base="layout")

class Index(object):
    def GET(self):
        return render.search_form()

    def POST(self):
        form = web.input(query="No Query")
        query = "Hello, %s" % form.query

        return render.index(query = query)

if __name__ == "__main__":
    app.run()