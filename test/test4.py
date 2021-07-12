import sys
import threading
from queue import PriorityQueue, Queue

class ExThread(threading.Thread):
    def __init__(self, bucket):
        threading.Thread.__init__(self)
        self.bucker = bucket
    
    def run(self):
        try:
            raise Exception("An error occured here.")
        except Exception:
            self.bucker.put(sys.exc_info())  # 把异常信息放入队列传递给父进程

def main():
    bucker = Queue()
    thread_obj = ExThread(bucker)
    thread_obj.start()

    while True:
        try:
            exc = bucker.get(block=False)
        except Queue.empty:
            pass
        else:
            exec_type, exec_obj, exec_trace = exc
            print("exc", exc) # exc (<class 'Exception'>, Exception('An error occured here.',), <traceback object at 0x7fb83bb3b848>)
            print("exec_type", exec_type) # exec_type <class 'Exception'>
            print("exec_obj", exec_obj)   # exec_obj An error occured here.
            print("exec_trace", exec_trace) #exec_trace <traceback object at 0x7f4b4584b908>
        thread_obj.join(0.1)
        if thread_obj.isAlive():
            continue
        else:
            break

if __name__ == "__main__":
    main()