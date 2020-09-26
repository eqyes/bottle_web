
#/usr/bin/env python
#coding=utf-8
from bottle import run,route,request,response
from bottle import template,view,static_file
from bottle import error,abort,redirect,default_app
from beaker.middleware import SessionMiddleware
from user import read_user
from user import write_user
from user import password_crypt

# define image path
images_path = './images'
assets_path = './assets'

# define download path
download_path = './download'

# define upload path
save_path = './upload'


# set session param
session_opts = {
    'session.type':'file',                   # 以文件的方式保存session
    'session.cookei_expires':3600,       # session过期时间为3600秒
    'session.data_dir':'/tmp/sessions',  # session存放路径
    'sessioni.auto':True
    }

@error(404)
def miss(code):
    # error page, generally can point to a 404 html page, then return, template('404') to access 404
    return '没找到页面！'

@route('/error')
def nofound():
    # cause 404 error
    abort(404)

@route('/page')
def page():
    # access /page, jump to main
    redirect('/')

# file upload html template, write here direct for easy
@route('/upload')
def upload():
    return '''
        <html>
            <head>
            </head>
            <body>
                <form action"/upload" method="post" enctype="multipart/form-data">
                    <input type="file" name="data" />
                    <input type="submit" value="Upload" />
                </form>
            </body>
        </html>
    '''

# file upload, overwrite=True override all orign file
# if no this param, when same file exists, return “IOError: File exists.” error
@route('/upload', method = 'POST')
def do_upload():
    upload = request.files.get('data')
    import os.path
    name, ext = os.path.splitext(upload.filename)  # use os.path.splitext separate file name and suffix 
    upload.filename = ''.join(('123',ext))        # change filename
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    upload.save(save_path, overwrite=True)  # file save to save_path 
    return u'upload success filename ：%s  suffix：%s \n changed file name：%s' %(name,ext,''.join(('123',ext)))

# force file download
@route('/download/<filename:path>')
def download(filename):
    return static_file(filename, root=download_path, download=filename)


@route('/assets/<filename:re:.*\.css|.*\.js|.*\.png|.*\.jpg|.*\.gif>')
def server_static(filename):
    """define /assets/ static(css,js,image) resource path"""
    return static_file(filename, root=assets_path)

@route('/assets/<filename:re:.*\.ttf|.*\.otf|.*\.eot|.*\.woff|.*\.svg|.*\.map>')
def server_static(filename):
    """define /assets/ font resource path"""
    return static_file(filename, root=assets_path)

@route('/images/<filename:re:.*\.png>')
def server_static(filename):
    return static_file(filename, root=images_path)

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
    data = {'tname':name,'tage':age,'tblog':blog, 'tqq': qq,'tbook':book,'tprice':price,'tnum':''}
    return data

@route('/logout')
def logout_get():
    password = ' '
    response.set_cookie('password', password, secret = 'psafe', httponly = True, max_age = 600)

    return redirect('/login')

#@route('/login', method = 'GET')
@route('/login')
def login_get():
    username = request.get_cookie('username', secret = 'usafe')
    password = request.get_cookie('password', secret = 'psafe')

    if read_user(username, password):
        return 'you already login'

    return template('login')

#@route('/login')
#def login():
#    return '''
#        <html>
#        <head>
#        </head>
#        <body>
#        <form action="/login" method="post">
#            Username: <input name="username" type="text" />
#            Password: <input name="password" type="password" />
#            <input value="Login" type="submit" />
#        </form>
#        </body>
#        </html>
#    '''

@route('/login', method = 'POST')
def login_post():
    username = request.forms.get('username')
    password = request.forms.get('password')
    password = password_crypt(password)

    if read_user(username, password):
        response.set_cookie('username', username, secret = 'usafe', httponly = True, max_age = 600)
        response.set_cookie('password', password, secret = 'psafe', httponly = True, max_age = 600)
        # correct get env beaker.session save to s, then we use dirt way save  data in s ,etc. username, id, authority
        s = request.environ.get('beaker.session')
        s['user'] = username
        s.save()
        return redirect('/')

    return redirect('/login')

@route('/')
def index():
    # for k,v in request.environ.items():
    #     print(k,v)
    s = request.environ.get('beaker.session') # get session
    username = s.get('user',None)   # get key as user value from session，which login to save
    if not username:
        return redirect('/login')

    return template('index')


app = default_app()
app = SessionMiddleware(app, session_opts)
run(app=app,host='0.0.0.0', port=8090,debug=True)
