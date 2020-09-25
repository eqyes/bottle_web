#main.py （文件名）

from bottle import run,route,template,request

@route("/login", method = 'get')

def index():
    return template('login')

@route('/login', method = 'post')
def index():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if username == 'admin' and password == 'root' :
        return f'wellcom {username}'
    return 'user or password error'

run(host='0.0.0.0', port=8090, debug=True, reloader=True)