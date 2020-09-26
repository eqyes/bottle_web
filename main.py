#!/usr/bin/env python
#coding=utf-8
from bottle import run,route,request,response
from bottle import template,view,static_file
from bottle import error,abort,redirect,default_app
from beaker.middleware import SessionMiddleware
from user import read_user
from user import write_user
from user import password_crypt

import os
import pymysql
pymysql.install_as_MySQLdb()

import MySQLdb
import logging

# define image path
images_path = './images'
assets_path = './assets'

# define download path
download_path = './download'

# define upload path
save_path = './upload'

pro_path = os.path.split(os.path.realpath(__file__))[0]
# define error log path
error_log = '/'.join((pro_path,'log/task_error.log'))

# define log print format
logging.basicConfig(level=logging.ERROR,
        format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        datefmt = '%Y-%m-%d %H:%M:%S',
        filename = error_log,
        filemode = 'a')

# define databash param
db_name = 'bottle_web'
db_user = 'root_sql'
db_pass = 'isokdo'
db_ip = 'localhost'
db_port = 3306


# define image path
images_path = './images'
assets_path = './assets'

# define download path
download_path = './download'

# define upload path
save_path = './upload'


# set session param
session_opts = {
    'session.type':'file',                   # use file to save session
    'session.cookei_expires':6,       # session timeout 3600 sec
    'session.data_dir':'/tmp/sessions',  # session save path
    'sessioni.auto':True
    }

@error(404)
def miss(code):
    # error page, generally can point to a 404 html page, then return, template('404') to access 404
    return 'page miss'

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
# if no this param, when same file exists, return ¡°IOError: File exists.¡± error
@route('/upload', method = 'POST')
def do_upload():
    upload = request.files.get('data')
    name, ext = os.path.splitext(upload.filename)  # use os.path.splitext separate file name and suffix 
    upload.filename = ''.join(('123',ext))        # change filename
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    # file save to save_path 
    upload.save(save_path, overwrite=True)
    return 'PASS'
#    return ('upload success filename £º%s  suffix£º%s \n changed file name£º%s' % (name, ext, ''.join(('123',ext))))

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
    username = 'y'
    password = 'y'
    response.set_cookie('password', password, secret = 'psafe', httponly = True, max_age = 600)
    s = request.environ.get('beaker.session') # get session
    del[s['user']]
    s.save()

    return redirect('/login')

#@route('/login', method = 'GET')
@route('/login')
def login_get():
    username = request.get_cookie('username', secret = 'usafe')
    password = request.get_cookie('password', secret = 'psafe')

    if read_user(username, password):
        return 'you already login'

    return template('login')

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
    username = s.get('user', None)   # get key as user value from session£¬which login to save
    if not username:
        return redirect('/login')

    return template('index')

def writeDb(sql,db_data=()):
    """
    connect mysql (write), and do write
    """
    try:
        conn = MySQLdb.connect(db=db_name,user=db_user,passwd=db_pass,host=db_ip,port=int(db_port))
        cursor = conn.cursor()
    except Exception as e:
        print(e)
        logging.error('database connect fail:%s' % e)
        return False

    try:
        cursor.execute(sql,db_data)
        conn.commit()
    except Exception as e:
        conn.rollback()
        logging.error('data write fail:%s' % e)
        return False
    finally:
        cursor.close()
        conn.close()
    return True


def readDb(sql,db_data=()):
    """
    connect mysql (from), data search
    """
    try:
        conn = MySQLdb.connect(db=db_name,user=db_user,passwd=db_pass,host=db_ip,port=int(db_port))
        cursor = conn.cursor()
    except Exception as e:
        print(e)
        logging.error('database connect faile:%s' % e)
        return False

    try:
        cursor.execute(sql,db_data)
        data = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
    except Exception as e:
        logging.error('data exec fail:%s' % e)
        return False
    finally:
        cursor.close()
        conn.close()
    return data


@route('/api/getuser',method="POST")
def getuser():
    sql = "select * from user;"
    userlist = readDb(sql,)
    return json.dumps(userlist)


@route('/adduser', method = 'GET')
def adduser_get():
    return template('adduser')

@route('/adduser',method="POST")
def adduser():
    name         = request.forms.get("name")
    age          = request.forms.get("age")
    sex          = request.forms.get("sex")
    qq           = request.forms.get("qq")
    email        = request.forms.get("email")
    department   = request.forms.get("department")

    if not name or not age or not sex or not qq or not email or not department:
        return '-2'

    sql = """
            INSERT INTO
                user(name,age,sex,qq,email,department)
            VALUES(%s,%s,%s,%s,%s,%s)
        """

    data = (name,age,sex,qq,email,department)
    print(data)
    result = writeDb(sql,data)
    if result:
        return '0'
    else:
        return '-1'

app = default_app()
app = SessionMiddleware(app, session_opts)
run(app=app,host='0.0.0.0', port=8090,debug=True)
