from peewee import PostgresqlDatabase, Model, TextField, IntegerField, BooleanField, \
    PrimaryKeyField, ForeignKeyField, CompositeKey
from playhouse.postgres_ext import ArrayField


db = PostgresqlDatabase(None)


class BaseModel(Model):
    class Meta:
        database = db


class Names(BaseModel):
    nconst = TextField(primary_key=True)
    primary_name = TextField()
    birth_year = IntegerField()
    death_year = IntegerField()
    primary_profession = TextField()
    known_for_titles = ArrayField(TextField)

    class Meta:
        db_table = 'names'


class Titles(BaseModel):
    tconst = TextField(primary_key=True)
    title_type = TextField()
    primary_title = TextField()
    original_title = TextField()
    is_adult = BooleanField()
    start_year = IntegerField()
    end_year = IntegerField()
    runtime_mins = IntegerField()
    genres = TextField()

    class Meta:
        db_table = 'titles'


class ManyNamesHasManyTitles(BaseModel):
    id_titles = ForeignKeyField(db_column='id_titles', rel_model=Titles)
    id_names = ForeignKeyField(db_column='id_names', rel_model=Names)

    class Meta:
        db_table = 'names_to_titles'
