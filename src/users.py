#coding:utf-8

import tornado.web


def authorized(url='/admin/login'):
    def wrap(handler):
        def authorized_handler(self, *args, **kw):
            request = self.request
            user_name_cookie = self.get_cookie('username','')
            user_pw_cookie = self.get_cookie('userpw','')
            if user_name_cookie and user_pw_cookie:
                from model import User
                user = User.check_user(user_name_cookie, user_pw_cookie)
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
