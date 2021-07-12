def is_isbn_or_key(q):
    """
       isbn: 13个0到9的数字组成
       isbn10: 10个0到9数字组成， 含有一些 '-'
    """
    isbn_or_key = 'key'
    if len(q) == 13 and q.isdigit():
        isbn_or_key = 'isbn'
    short_q = q.replace('-', '')
    if '-' in q and len(short_q) == 10 and short_q.isdigit():
        isbn_or_key = 'isbn'
    return isbn_or_key
