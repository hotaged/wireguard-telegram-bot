from os import environ


token = environ.get('TOKEN')
db_uri = environ.get('DB_URI')
debug = environ.get('DEBUG') == '1'


# postgres://wgbot:AAFaBvgZBIskLA6G6ABg1hgZwpEhNJtGDUg@127.0.0.1:5432/wgbot


if token is None:
    raise ValueError('Environment variable `TOKEN` was not specified.')

if db_uri is None:
    raise ValueError('Environment variable `DB_URI` was not specified.')

