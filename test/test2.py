from werkzeug.local import LocalStack

s = LocalStack()
s.push(1)
print(s.top)
print(s.top)
print(s.pop())
print(s.top)  # None

s.push(1)
s.push(2)
print(s.top)   #2
print(s.top)   #2
print(s.pop()) #2
print(s.top)   #1
