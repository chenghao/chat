#coding:utf-8

import tornado.web
import tornado.websocket
import json
import uuid

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class SocketHandler(tornado.websocket.WebSocketHandler):
    """docstring for SocketHandler"""
    clients = set()
    client_map = {}

    @staticmethod
    def send_to_all(self, message):
        ''' 发送给所有的客户端 '''
        for i in SocketHandler.client_map:
            SocketHandler.client_map[i].write_message(json.dumps(message))

    @staticmethod
    def send_only(p2pClients, message):
        ''' 发送给某个客户端 '''
        for p2pClient in p2pClients:
            p2pClient.write_message(json.dumps(message))
     
        
    def open(self):        
        self.write_message(json.dumps({
            'type': 'sys',
            'message': 'Welcome to WebSocket id: ' + str(id(self)),
        }))
        SocketHandler.send_to_all(
            self,
            {
                'type': 'sys',
                'message': 'id ' + str(id(self)) + ' has joined',
            }
        )
        SocketHandler.client_map[id(self)] = self

    def on_close(self):
        del SocketHandler.client_map[id(self)]
        SocketHandler.send_to_all(self, {
            'type': 'sys',
            'message': 'id ' + str(id(self)) + ' has left',
        })

    def on_message(self, message):
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
                'id': id(self),
                'message': s[0],
            })      
            

urls = [
    (r"/", IndexHandler),
    (r"/chat", SocketHandler)
]
