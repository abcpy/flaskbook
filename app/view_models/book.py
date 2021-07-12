class BookViewBodel:
    def __init__(self, book) -> None:
        self.title = book['title']
        self.isbn = book['isbn']
        self.cover_url = book['cover_url']
        self.book_intro = book['book_intro']
        self.comments = book['comments']
        self.author_intro = book['author_intro']
        self.publisher = book['book_info']['出版社']
        self.price = book['book_info']['定价']
        self.author = book['book_info']['作者']
        self.pages = book['book_info']['页数']
        self.pubdate = book['book_info']['出版年']
        self.binding = book['book_info']['装帧']
    
    @property
    def intro(self):
        intros = filter(lambda x: True if x else False, [self.author, self.publisher, self.price])
        return '/'.join(intros)


class BookCollection:
    def __init__(self) -> None:
        self.total = 0
        self.books = []
        self.keyword = ''
    
    def fill(self, yushu_book, keyword):
        self.total = yushu_book.total
        self.keyword = keyword
        self.books = [BookViewBodel(book) for book in yushu_book.books]