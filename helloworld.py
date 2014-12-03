
from google.appengine.api import files
from google.appengine.ext import db


import webapp2

class pongy(db.Model):
    booo = db.StringProperty(required=True)
    test = db.StringProperty(required=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        filename = '/gs/pong_bucket/test.txt'

        writable_file_name = files.gs.create(filename, mime_type='text/html', acl='public-read')

        with files.open(writable_file_name, 'a') as f:
            f.write('Hello World')
        files.finalize(writable_file_name)
        with files.open(filename, 'r') as f:
            print f.read()

        q = pongy.all()
        q.filter('test =', 'testing123')
        for p in q.run():
            if not p:
                p = pongy(test='testing123', booo='boooo1234')
                p.put()

        q = pongy.all()
        for item in q.run():
            print item.booo
            print item.test
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello World!')

application = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)