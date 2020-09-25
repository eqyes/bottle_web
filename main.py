# main.py

from bottle import run,route,template

@route("/<name>")

def index(name):

    return template('index',username = name)

run(host='0.0.0.0', port=8090, debug=True, reloader=True)