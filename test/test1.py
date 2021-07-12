import threading
import time
from werkzeug.local import Local, LocalStack

"""
线程隔离对象
"""
class A:
    b = 1

# my_obj = A()
my_obj = Local()
my_obj.b = 1

def worker():
    my_obj.b = 2
    print('new thread my_obj', my_obj.b)

new_t = threading.Thread(target=worker)
new_t.start()
time.sleep(1)

#主线程
print('main thread my_obj', my_obj.b) 
# new thread my_obj 2
# main thread my_obj 1 
# 结果为2

