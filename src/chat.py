#coding:utf-8

import tornado.web
import tornado.websocket
import json
from dbutil import authorized, User

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class IndexHandler(tornado.web.RequestHandler):
    @authorized()
    def get(self):
        self.render("index.html")

class SocketHandler(tornado.websocket.WebSocketHandler):
    """docstring for SocketHandler"""
    client_map = {}
    users_map = {}

    @staticmethod
    def send_to_all(self, message):
        """发送给所有的客户端"""
        for i in SocketHandler.client_map:
            SocketHandler.client_map[i].write_message(json.dumps(message))

    @staticmethod
    def send_only(p2pClients, message):
        """发送给某个客户端"""
        for p2pClient in p2pClients:
            p2pClient.write_message(json.dumps(message))

    def open(self):
        loginName = self.get_cookie("loginName", "")
        user = User.get_user_by_name(loginName)

        SocketHandler.client_map[user.serial] = self
        User.update_user_status(user.loginName, 2)

        users = {}
        users["nickName"] = user.nickName.encode('utf-8')
        users["serial"] = user.serial
        SocketHandler.users_map[loginName] = users

        self.write_message(json.dumps({
            'type': 'sys',
            'user': user.nickName.encode('utf-8'),
        }))

        SocketHandler.send_to_all(
            self,
            {
                'type': 'sys',
                'users_list': SocketHandler.users_map,
            }
        )

    def on_close(self):
        loginName = self.get_cookie("loginName", "")
        user = User.get_user_by_name(loginName)

        del SocketHandler.client_map[user.serial]
        del SocketHandler.users_map[loginName]
        User.update_user_status(user.loginName, 1)

        SocketHandler.send_to_all(self, {
            'type': 'sys',
            'users_list': SocketHandler.users_map,
        })

    def on_message(self, message):
        loginName = self.get_cookie("loginName", "")
        user = User.get_user_by_name(loginName)

        try:
            message_map = eval(str(message))
            p2pClients = (SocketHandler.client_map.get(user.serial), SocketHandler.client_map.get(message_map["serial"]))
            SocketHandler.send_only(
                p2pClients,
                {
                    'type': 'user',
                    'id': user.serial,
                    'message': user.nickName.encode("utf-8") + " 说：" + message_map["msg"],
                }
            )
        except:
            SocketHandler.send_to_all(self, {
                'type': 'user',
                'id': user.serial,
                'message': user.nickName.encode("utf-8") + " 说：" + message,
            })


urls = [
    (r"/", IndexHandler),
    (r"/chat", SocketHandler)
]
