#coding:utf-8

import torndb
from hashlib import md5

import sqlite3
import models

DBHOST = "localhost"
DBPORT = 3306
DBUSER = "root"
DBPWD = "0123456789"
#DBPWD = "hao"
DBNAME = "chat"

"""
conn = torndb.Connection("%s:%s" % (DBHOST, str(DBPORT)), DBNAME, DBUSER, DBPWD)
cursor = conn._cursor()
"""
conn = sqlite3.connect("chat.db")
conn.text_factory = str
cursor = conn.cursor()


def authorized(url='/login'):
    def wrap(handler):
        def authorized_handler(self, *args, **kw):
            request = self.request
            user_login_name_cookie = self.get_cookie('loginName', '')
            user_password_cookie = self.get_cookie('password', '')
            if user_login_name_cookie and user_password_cookie:
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

    def __init__(self, conn):
        create_table_sql = """
          CREATE TABLE IF NOT EXISTS `user` (
            `loginName` TEXT NOT NULL ,
            `password` TEXT NOT NULL ,
            `nickName` TEXT NOT NULL ,
            `serial` TEXT NOT NULL ,
            `status` INTEGER DEFAULT '1'
          ) """
        conn.execute(create_table_sql)

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
        """
        conn._ensure_connected()
        return conn.get('SELECT * FROM `user` WHERE `loginName` = \'%s\' LIMIT 1' % str(loginName))
        """
        user = conn.execute('SELECT * FROM `user` WHERE `loginName` = \'%s\' LIMIT 1' % str(loginName)).fetchone()
        if user:
            user1 = models.User(user[0], user[1], user[2], user[3], user[4])
            return user1
        else:
            return None


    def add_user(self, loginName, password, nickName, serial):
        if loginName and password and nickName and serial:
            '''
            sql = "insert into user (loginName, password, nickName, serial) values(%s, %s, %s, %s)"
            conn._ensure_connected()
            return conn.execute(sql, loginName, md5(password.encode('utf-8')).hexdigest(), nickName, serial)
            '''
            sql = "insert into user (loginName, password, nickName, serial) values(?, ?, ?, ?)"
            c = conn.execute(sql, (loginName.encode('utf-8'), md5(password.encode('utf-8')).hexdigest(), nickName.encode('utf-8'), str(serial)))
            conn.commit()
            return c.rowcount
        else:
            return None

    def update_user_status(self, loginName, status):
        if loginName and status:
            '''
            sql = "update user set status = %s where loginName = %s"
            conn._ensure_connected()
            return conn.execute(sql, status, loginName)
            '''
            sql = "update user set status = ? where loginName = ?"
            c = conn.execute(sql, (status, loginName))
            conn.commit()
            return c.rowcount
        else:
            return None

#User = User()
User = User(conn)

