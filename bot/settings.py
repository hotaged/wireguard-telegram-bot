from os import environ


token = environ.get('TOKEN')
db_uri = environ.get('DB_URI')
debug = environ.get('DEBUG') == '1'


if db_uri is None:
    db_uri = 'postgres://wgbot:AAFaBvgZBIskLA6G6ABg1hgZwpEhNJtGDUg@127.0.0.1:5432/wgbot'

if debug is None:
    debug = False

