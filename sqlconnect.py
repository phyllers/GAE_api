import os
import MySQLdb

env = os.getenv('SERVER_SOFTWARE')
if env and env.startswith('Google App Engine/'):
    # Connecting from App Engine
    db = MySQLdb.connect(
        unix_socket='/cloudsql/striking-berm-771:django-test',
        user='root',
        name='pong',
    )
else:
    # Connecting from an external network.
    # Make sure your network is whitelisted
    db = MySQLdb.connect(host='127.0.0.1', port=3306, user='root')

cursor = db.cursor()
cursor.execute('SELECT 1 + 1')
