from flask import request, jsonify, abort
from peewee import SQL
from . import mod_movies
from imdb_rest.models import Names, Titles, ManyNamesHasManyTitles


@mod_movies.route('/movies_by_start_year')
def movies_by_start_year():
    """ Retrieves list (in alphabetical order) with
    all titles of movies indicated by 'start_year' value
    and corresponding names (actors 'primary_name').
    Accepts 'year' and 'page' request arguments.
    """
    titles = Titles.select(Titles.original_title, Titles.tconst)
    if not request.args.get('year') or not request.args.get('page'):
        abort(400)
    try:
        year = int(request.args.get('year'))
        page = int(request.args.get('page'))
    except ValueError:
        abort(400)
    titles = titles.where(Titles.start_year==year)
    titles = titles.order_by(Titles.original_title.asc()).paginate(page, 20).dicts()
    response = []
    # N+1 queries (20)
    for title in titles:
        names = Names.select(
            Names.primary_name
        ).join(
            ManyNamesHasManyTitles
        ).where(
            ManyNamesHasManyTitles.id_titles==title['tconst']
        ).dicts()
        title['names'] = [name['primary_name'] for name in names]
        del title['tconst']
        response.append(title)
    return jsonify({'titles': response})


@mod_movies.route('/movies_by_genre')
def movies_by_genre():
    """ Retrieves list (in alphabetical order) with
    all titles of movies indicated by 'genre' value
    and corresponding names (actors 'primary_name').
    Accepts 'genre' and 'page' request arguments.
    """
    titles = Titles.select(Titles.original_title, Titles.tconst)
    if not request.args.get('genre') or not request.args.get('page'):
        abort(400)
    titles = titles.where(SQL('%s = ANY("t1"."genres")', request.args.get('genre')))
    try:
        page = int(request.args.get('page'))
    except ValueError:
        abort(400)
    titles = titles.order_by(Titles.original_title.asc()).paginate(page, 20).dicts()
    response = []
    # N+1 queries (20)
    for title in titles:
        names = Names.select(
            Names.primary_name
        ).join(
            ManyNamesHasManyTitles
        ).where(
            ManyNamesHasManyTitles.id_titles==title['tconst']
        ).dicts()
        title['names'] = [name['primary_name'] for name in names]
        del title['tconst']
        response.append(title)
    return jsonify({'titles': response})


@mod_movies.route('/movies_by_name')
def movies_by_name():
    """ Retrieves list (in alphabetical order) with
    all actors indicated by 'primary_name' value
    and corresponding titles (titles 'original_title').
    Accepts 'name' and 'page' request arguments.
    """
    primary_name = '%'+request.args.get('name')+'%'
    names = Names.select(Names.primary_name, Names.nconst)
    if not request.args.get('name') or not request.args.get('page'):
        abort(400)
    try:
        primary_name = '%'+request.args.get('name')+'%'
        names = names.where(Names.primary_name ** primary_name)
        page = int(request.args.get('page'))
        names = names.order_by(Names.primary_name.asc()).paginate(page, 20).dicts()
    except ValueError:
        abort(400)
    response = []
    # N+1 queries (20)
    for name in names:
        titles = Titles.select(
            Titles.original_title
        ).join(
            ManyNamesHasManyTitles
        ).where(
            ManyNamesHasManyTitles.id_names==name['nconst']
        ).dicts()
        name['titles'] = [title['original_title'] for title in titles]
        del name['nconst']
        response.append(name)
    return jsonify({'titles': response})
