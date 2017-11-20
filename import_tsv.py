""" Import imdb open .tsv data to PostgreSQL database.
Files to import (name.basics.tsv, title.basics.tsv)
should be in the same path as import_tsv.py script.
"""
import psycopg2
import csv
import time


st = time.time()

print('Creating db tables...')
connection = psycopg2.connect(
    host='localhost',
    dbname='imdb-import',
    port='5432',
    user='luq',
    password='fourwordsalluppercase'
)
cursor = connection.cursor()

# Create db tables if not exists
cursor.execute(
    '''CREATE TABLE IF NOT EXISTS names
    (
        nconst text,
        primary_name text,
        birth_year integer,
        death_year integer,
        primary_profession text,
        known_for_titles text
    )'''
)
cursor.execute(
    '''CREATE TABLE IF NOT EXISTS titles
    (   
        tconst text,
        title_type text,
        primary_title text,
        original_title text,
        is_adult bool,
        start_year integer,
        end_year integer,
        runtime_mins integer,
        genres text
    )'''
)

# Clear tables if importing data one more time
cursor.execute('TRUNCATE TABLE names')
cursor.execute('TRUNCATE TABLE titles')

print('Copying data...')
with open('name.basics.tsv') as names:
    # Omit header
    names.readline()
    cursor.copy_from(names, 'names',
        columns=('nconst','primary_name','birth_year','death_year', 'primary_profession', 'known_for_titles')
    )

with open('title.basics.tsv') as titles:
    # Omit header
    titles.readline()
    cursor.copy_from(titles, 'titles',
        columns=('tconst','title_type','primary_title','original_title', 'is_adult', 'start_year', 'end_year', 'runtime_mins', 'genres')
    )

# Commit and close connection
print('Saving data...')
connection.commit()
connection.close()

print('Executed in (sec):', time.time() - st)
