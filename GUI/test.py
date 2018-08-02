import signal
import tornado.ioloop
import tornado.web
import tornado.escape
import os
import base64
import time
import json

TIMEOUT = 5

cookie_code = base64.b64encode(os.urandom(50)).decode('ascii')
print("Cookie code: " + cookie_code)


def interrupted(signum, frame):
    print("TRAVIS")
    exit(0)


signal.signal(signal.SIGALRM, interrupted)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", title="Smarthome")


class RootHandler(tornado.web.RequestHandler):
    def get(self):
        if not self.get_secure_cookie("Cookie_monster"):
            print("Someone is trying to gain access without password!")
            self.render("index.html", title="Smarthome")
        else:
            self.render("static/root.html", title="Luca")


class Root1Handler(tornado.web.RequestHandler):
    def get(self):
        if not self.get_secure_cookie("Cookie_monster"):
            print("Someone is trying to gain access without password!")
            self.render("index.html", title="Smarthome")
        else:
            self.render("static/root1.html", title="Federico")


class LoginHandler(tornado.web.RequestHandler):
    def post(self):
        data = json.loads(self.request.body)
        user = data['myUser']
        password = data['myPass']
        print(user)
        print(password)
        if user == "Luca" and password == "ciccio":
            print(user + " gained access")
            self.set_secure_cookie("Cookie_monster", "Luca", expires_days=7)
            self.redirect("/root", status=303)
        elif user == "Fede" and password == "pippo":
            print(user + " gained access")
            self.set_secure_cookie("Cookie_monster", "Federico", expires_days=7)
            self.redirect("/root1", status=303)
        else:
            print("Wrong password")
            self.write('403 Forbidden')



class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/(favicon.ico)', tornado.web.StaticFileHandler, {"path": ""}),
            (r'/', MainHandler),
            (r'/index.html', MainHandler),
            (r'/root', RootHandler),
            (r'/root1', Root1Handler),
            (r'/login', LoginHandler)
        ]
        settings = {
            "debug": True,
            "static_path": os.path.join(os.path.dirname(__file__), "static"),
            "cookie_secret": cookie_code
        }
        tornado.web.Application.__init__(self, handlers, **settings)


print("OK")
print("Build succeded!")
signal.alarm(TIMEOUT)
travis = int(input("Write 1: "))
signal.alarm(0)

try:
    http_server = tornado.httpserver.HTTPServer(Application(),
                                                # ssl_options={
        # "certfile": "/var/pyTest/keys/ca.csr",
        # "keyfile": "/var/pyTest/keys/ca.key",
    # })
    )
    http_server.listen(8080)
    # http_server.listen(80) TODO http standard
    # http_server.listen(443) TODO ssl
    tornado.ioloop.IOLoop.instance().start()
except KeyboardInterrupt:
    print("\nClosing...")
    time.sleep(2)
    exit()
except Exception as global_error:
    print(global_error)
    exit(1)