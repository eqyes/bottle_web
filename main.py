#main.py

from bottle import run,route,template,request,response
from user import read_user
from user import write_user
from user import password_crypt

@route('/login', method = 'GET')
def login_get():
    username = request.get_cookie('username', secret = 'usafe')
    password = request.get_cookie('password', secret = 'psafe')

    if read_user(username, password):
        return 'you already logout'

    return template('login')

@route('/login', method = 'POST')
def login_post():
    username = request.forms.get('username')
    password = request.forms.get('password')
    password = password_crypt(password)

    if read_user(username, password):
        response.set_cookie('username', username, secret = 'usafe', httponly = True, max_age = 600)
        response.set_cookie('password', password, secret = 'psafe', httponly = True, max_age = 600)
        return 'login success'

    return 'user or password wrong'

@route('/register', method = 'GET')
def register_get():
    return template('register')

@route('/register', method = 'POST')
def register_post():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if read_user(username, password, nopwd = True):
        write_user(username, password)
        return 'success'

    return 'register faild'

run(host='0.0.0.0', port=8090, debug=True, reloader=True)