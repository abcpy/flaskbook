from werkzeug.local import LocalStack
import threading
import time

my_stack = LocalStack()
my_stack.push(1)
print('in main thread after push, value is:', str(my_stack.top))

def worker():
    # 新线程
    print('in new thread before push, value is:', str(my_stack.top))
    my_stack.push(2)
    print('in new thread after push, value is:', str(my_stack.top))

new_t = threading.Thread(target=worker)
new_t.start()
time.sleep(1)

# 主线程
print('in main thread after push, value is:', str(my_stack.top))

"""
  in main thread after push, value is: 1
in new thread before push, value is: None
in new thread after push, value is: 2
in main thread after push, value is: 1
"""


