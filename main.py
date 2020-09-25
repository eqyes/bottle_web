#main.py

from bottle import run,route,request,response
from bottle import template,view
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

@route('/info')
@view('info')     #use view load info template, no need write template suffix
def info():
    name = 'isokdo'
    age = '30'
    blog = 'www.isokdo.com'
    qq = '254758987'
    book = ['python','linux','php']
    price = {'pc':4000,'phone':2000,'bike':600}
    data = {'tname':name,'tage':age,'tblog':blog, 'tqq': qq,'tbook':book,'tprice':price}
    return data

run(host='0.0.0.0', port=8090, debug=True, reloader=True)
