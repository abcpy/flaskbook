from app.libs.download import HTTP
from flask import current_app

class YuShuBook:
    isbn_url = 'https://api.feelyou.top/isbn/{}'
    keyword_url = 'https://api.feelyou.top/search?q={}&count={}&start={}'

    def __init__(self) -> None:
        self.total = 0
        self.books = []

    def search_by_isbn(self, isbn):
        url = self.isbn_url.format(isbn)
        # print("url", url)
        result = HTTP.get(url)
        # print(result)
        self.__fill_single(result)
    
    def __fill_single(self, data):
        if data:
            print(data)
            self.total = 1
            self.books.append(data)
    
    @property
    def first(self):
        return self.books[0] if self.total >=1 else None
    
    @classmethod
    def search_by_keywod(cls, keyword, page=1):
        url = cls.keyword_url.format(keyword, current_app.config['PER_PAGE'], cls.calculate_start(page))
        return HTTP.get(url)
    
    @staticmethod
    def calculate_start(page):
        return (page - 1) * current_app.config['PER_PAGE']

    