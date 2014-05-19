#coding:utf-8

import tornado.web
from hashlib import md5
from dbutil import User

class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("login.html")

    def post(self):
        try:
            loginName = self.get_argument("loginName")
            password = self.get_argument("password")
        except:
            self.redirect('/login')
            return
        if loginName and password:
            password = md5(password.encode('utf-8')).hexdigest()
            user = User.check_user( loginName, password)
            if user:
                #logging.error('user ok')
                self.set_cookie('loginName', loginName, path="/", expires_days = 365 )
                self.set_cookie('password', password, path="/", expires_days = 365 )
                self.redirect('/')
                return
            else:
                #logging.error('user not ok')
                self.redirect('/login')
                return
        else:
            self.redirect('/login')


urls = [
    (r"/login", LoginHandler)
]