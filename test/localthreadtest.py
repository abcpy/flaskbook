import threading

storage = threading.local()
storage.foo = 1
print(storage.foo)  #1

class ChildThread(threading.Thread):
    def run(self):
        storage.foo = 2
        print("child thread", storage.foo)  # child thread 2

chthread = ChildThread()
chthread.start()
print(threading.get_ident()) # 140154346604352

print("main thread:", storage.foo) # main thread: 1

from flask import Flask, current_app
from flask.globals import _app_ctx_stack, _request_ctx_stack

app = Flask(__name__)
print(_app_ctx_stack.top)  # None
print(_request_ctx_stack.top) # None
# print(_app_ctx_stack())  #RuntimeError: object unbound
# print(current_app)
ctx = app.app_context()
ctx.push()
print(_app_ctx_stack.top) # <flask.ctx.AppContext object at 0x7fd6d88874e0>
print(_app_ctx_stack.top is ctx) # True
print(current_app) # <Flask 'localthreadtest'>


