# -*- coding:UTF-8 -*-
import json
import uuid

import tornado.web
import tornado.ioloop
import tornado.websocket

#http请求
class IndexHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render('index.html')


class ChatHandler(tornado.websocket.WebSocketHandler):
    # 用户存储当前聊天室用户
    waiters = set()
    # 用于存储历时消息
    messages = []

    def check_origin(self, origin):
        return True

    def open(self, *args, **kwargs):
        '''
        客户端和服务端已经建立链接,中间的过程框架已经帮我们做了
        链接
        握手
        :param args:
        :param kwargs:
        :return:
        '''
        ChatHandler.waiters.add(self)
        uid = str(uuid.uuid4())
        self.write_message(uid)

        for msg in ChatHandler.messages:
            content = self.render_string('message.html',**msg)
            self.write_message(content)

    # 接收客户端发的消息
    def on_message(self, message):
        '''
        客户端发送消息时，自动执行
        :param message:
        :return:
        '''
        msg = json.loads(message)
        ChatHandler.messages.append(message)

        for client in ChatHandler.waiters:
            content = client.render_string('message.html',**msg)
            client.write_message(content)



    # 主动关闭链接
    def on_close(self):
        ChatHandler.waiters.remove(self)



def run():
    settings = {
        'template_path': 'templates',
        'static_path': 'static',
    }
    application = tornado.web.Application([
        (r"/", IndexHandler),
        (r"/chat", ChatHandler),
    ], **settings)
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    run()















