import os
import MySQLdb
import json
import webapp2

from google.appengine.api import memcache, users
from google.appengine.ext import db
from google.appengine.ext.webapp.template import render
from google.appengine.ext.webapp.util import run_wsgi_app

env = os.getenv('SERVER_SOFTWARE')
if env and env.startswith('Google App Engine/') or os.getenv('SETTINGS_MODE') == 'prod':
    # Connecting from App Engine
    db = MySQLdb.connect(
        unix_socket='/cloudsql/striking-berm-771:django-test',
        db='pong',
        user='root',
    )
else:
    # Connecting from an external network.
    # Make sure your network is whitelisted
    db = MySQLdb.connect(host='127.0.0.1', port=3306, db='test', user='root')


# class Greeting(db.Model):
#     author = db.UserProperty()
#     content = db.TextProperty()
#     date = db.DateTimeProperty(auto_now_add=True)

class ListHandler(webapp2.RequestHandler):
    def get(self):
        cursor = db.cursor()
        cursor.execute('SELECT * from testapp_greeting;')
        data = []
        for row in cursor.fetchall():
            data.append({'id': row[0],
                         'content': row[2],
                         'date': row[3].isoformat()})

        variables = {'data': data}
        # j = json.dumps(data)
        # variables['json'] = j

        self.response.out.write(json.dumps(variables))

class ItemHandler(webapp2.RequestHandler):
    def get(self, item_id):
        try:
            int(item_id)
            cursor = db.cursor()
            cursor.execute('SELECT * FROM testapp_greeting WHERE id=%s;' % item_id)
            data = []
            for row in cursor.fetchall():
                data.append({'id': row[0],
                             'content': row[2],
                             'date': row[3].isoformat()})

            result = {'data': data}
            # j = json.dumps(data)
            # result['json'] = j
            result['item_id'] = item_id
        except:
            result = {'err': '%s incorrectly formatted'}

        self.response.out.write(json.dumps(result))

# class GuestBook(webapp2.RequestHandler):
#     def post(self):
#         greeting = Greeting()
#         greeting.content = self.request.get('content')
#         greeting.put()
#         memcache.delete('greetings')
#         self.redirect('/')

application = webapp2.WSGIApplication([
    ('/', ListHandler),
    ('/(\d+)', ItemHandler),
    # ('/sign', GuestBook),
], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()