#main.py

from bottle import run,route,template,request
from user import read_user

@route("/login", method = 'get')
def index():
    return template('login')

@route('/login', method = 'post')
def index():
    username = request.forms.get('username')
    password = request.forms.get('password')

    if read_user(username, password):
        return 'login success'
    return 'user or password error'

run(host='0.0.0.0', port=8090, debug=True, reloader=True)