import json

with open('credenciais.json') as arquivo_json:
    config = json.load(arquivo_json)

USER = config.get('USER')
PASSWORD = config.get('PASSWORD')
HOST = config.get('HOST')
PORT = config.get('PORT')
DATABASE = config.get('DATABASE')
DATABASE_URL = config.get('DATABASE_URL')
