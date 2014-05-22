#coding:utf-8
import uuid
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


class LogoutHandler(tornado.web.RequestHandler):
    def get(self):
        self.clear_all_cookies()
        self.redirect('/login')

class RegisterHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("register.html", msg="")

    def post(self):
        try:
            loginName = self.get_argument("loginName")
            password = self.get_argument("password")
            nickName = self.get_argument("nickName")
        except:
            self.redirect('/register')
            return
        if loginName and password and nickName:
            user = User.get_user_by_name(loginName)
            if user:
                self.render("register.html", msg="登录名已存在")
            else:
                serial = uuid.uuid4()
                user = User.add_user(loginName, password, nickName, serial)
                if user:
                    self.set_cookie('loginName', loginName, path="/", expires_days=365)
                    self.set_cookie('password', md5(password.encode('utf-8')).hexdigest(), path="/", expires_days=365)
                    self.redirect('/')
                    return
                else:
                    self.redirect('/login')
                    return
        else:
            self.redirect('/login')

urls = [
    (r"/login", LoginHandler),
    (r"/logout", LogoutHandler),
    (r"/register", RegisterHandler)
]