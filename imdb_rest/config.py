import os


class Config(object):
    DB_NAME = 'imdb-import'
    DB_USER = 'luq'
    DB_PASS = 'fourwordsalluppercase'
    DB_HOST = 'localhost'
    DB_PORT = '5432'


config = {
    'config' : Config
}