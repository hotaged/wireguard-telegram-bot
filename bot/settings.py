from os import environ


token = environ.get('TOKEN')
db_uri = environ.get('DB_URI')
debug = environ.get('DEBUG') == '1'


if db_uri is None:
    db_uri = 'sqlite://db.sqlite3'

if debug is None:
    debug = False

