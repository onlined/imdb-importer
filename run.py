from imdb_rest import create_app


if __name__ == '__main__':
    app = create_app('config')
    app.run(host='0.0.0.0', port=9500, debug=True, threaded=True)
