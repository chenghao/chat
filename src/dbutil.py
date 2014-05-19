#coding:utf-8

import torndb

DBHOST = "localhost"
DBPORT = 3306
DBUSER = "root"
DBPWD = "0123456789"
DBNAME = "chat"

conn = torndb.Connection("%s:%s" % (DBHOST, str(DBPORT)), DBNAME, DBUSER, DBPWD)
cursor = conn._cursor()

def authorized(url='/login'):
    def wrap(handler):
        def authorized_handler(self, *args, **kw):
            request = self.request
            user_login_name_cookie = self.get_cookie('loginName', '')
            user_password_cookie = self.get_cookie('password', '')
            if user_login_name_cookie and user_password_cookie:
                #from dbutil import User
                user = User.check_user(user_login_name_cookie, user_password_cookie)
            else:
                user = False
            if request.method == 'GET':
                if not user:
                    self.redirect(url)
                    return False
                else:
                    handler(self, *args, **kw)
            else:
                if not user:
                    self.error(403)
                else:
                    handler(self, *args, **kw)
        return authorized_handler
    return wrap

class User():
    def check_user(self, loginName='', password=''):
        if loginName and password:
            user = self.get_user_by_name(loginName)
            if user and user.loginName == loginName and user.password == password:
                return True
            else:
                return False
        else:
            return False

    def get_user_by_name(self, loginName):
        conn._ensure_connected()
        return conn.get('SELECT * FROM `user` WHERE `loginName` = \'%s\' LIMIT 1' % str(loginName))


User = User()


