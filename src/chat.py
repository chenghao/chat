#coding:utf-8

import os.path
import tornado.httpserver
import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpclient
import tornado.websocket
import json
import uuid

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

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
            
    
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
            (r"/chat", SocketHandler)
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

##MAIN
if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()