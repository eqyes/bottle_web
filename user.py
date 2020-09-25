#user.py
import os

from bcrypt import hashpw

SALT = b'$2b$10$8g62hrrYx4W11cQTuvi5ye'

if not os.path.exists('./userinfo.txt'):
    open('./userinfo.txt', 'w', encoding = 'utf-8').close()

def password_crypt(password):
    password = password.encode()
    cry_pwd = hashpw(password, SALT)

    return cry_pwd.decode()

def read_user(username, password, nopwd = False):
    userinfo = dict()

    with open('./userinfo.txt', 'r', encoding = 'utf-8') as fob:
        for line in fob.readlines():
            uname = line.strip().split('=>')[0]
            try:
                pwd = line.strip().split('=>')[1]
                userinfo[uname] = pwd
            except:
                print('\033[1;31;40m  fatal error: user info file format error, system can not run \033[0m')
                exit(1)

    if nopwd == True:
        if username in userinfo:
            return False
        else:
            return True

    if userinfo.get(username,False) == password:
        return True

    return False

def write_user(username, password):
    fob = open('./userinfo.txt', 'a', encoding = 'utf-8')
    fob.write(username + '=>' + password_crypt(password) + '\n')
    fob.close()

    return True