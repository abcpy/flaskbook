from contextlib import contextmanager

@contextmanager
def book_mark():
    print('《', end='')
    yield
    print('》', end='')

with book_mark():
    print('且将生活一饮而尽', end='')