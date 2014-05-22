#coding:utf-8

import tornado.web
import tornado.websocket
import json
import uuid

from dbutil import authorized, User


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
        print SocketHandler.users_map

        self.write_message(json.dumps({
            'type': 'sys',
            'message': '欢迎 ' + user.nickName.encode('utf-8') + ' 的到来',
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
        print message

        loginName = self.get_cookie("loginName", "")
        user = User.get_user_by_name(loginName)

        s = message.split("`")
        if len(s) == 2:
            p2pClients = (SocketHandler.client_map.get(int(s[0])), SocketHandler.client_map.get(id(self)))
            SocketHandler.send_only(
                p2pClients,
                {
                    'type': 'user',
                    'id': id(self),
                    'message': s[1],
                }
            )
        else:
            SocketHandler.send_to_all(self, {
                'type': 'user',
                'id': user.serial,
                'message': s[0],
            })


urls = [
    (r"/", IndexHandler),
    (r"/chat", SocketHandler)
]
