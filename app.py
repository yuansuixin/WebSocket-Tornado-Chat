# -*- coding:UTF-8 -*-
import tornado.web
import tornado.ioloop
import tornado.websocket

#http请求
class IndexHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render('index.html')


class ChatHandler(tornado.websocket.WebSocketHandler):
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
        print('来人了...')
    # 接收客户端发的消息
    def on_message(self, message):
        print(message)
        message = message+'fjdsafnasffia'
        # 发送数据给客户端
        self.write_message(message)

    # 主动关闭链接
    def on_close(self):
        pass



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














