from wtforms import form
from . import web
from app.spider.yushu_book import YuShuBook
from app.forms.book import SearchForm
from flask import jsonify, request, render_template, flash
from app.libs import util
from app.view_models.book import BookCollection, BookViewBodel
from app.models.gift import Gift
from app.models.wish import Wish
from app.view_models.trade import TradeInfo
from flask_login import current_user


"""
   register view function
"""
@web.route("/test")
def test():
    import pdb; pdb.set_trace() 
    r = {
        'name': '七月',
        'age': 18
    }
    flash('You were successfully logged in')
    return render_template('test.html', data=r)

@web.route("/book/search")
def search():
    """
       视图函数
       q:普通关键字 isbn 
    """
    form = SearchForm(request.args)
    books = BookCollection()

    if form.validate():
        q = form.q.data.strip()
        print(q)
        page = form.q.data
        isbn_or_key = util.is_isbn_or_key(q)
        yushu_book = YuShuBook()

        if isbn_or_key:
            print("isbn_or_key")
            yushu_book.search_by_isbn(q)
            # print(yushu_book.books[0]['book_info']['作者'])
        else:
            result  = YuShuBook.search_by_keywod(page)
        books.fill(yushu_book, q)
        # return json.dumps(books, default=lambda o:o.__dict__)
        # return jsonify(books.__dict__)
        # return render_template('search_result.html', books=books)
    else:
        flash('please input isbn')
    return render_template('search_result.html', books=books)

@web.route('/book/<isbn>/detail')
def book_detail(isbn):

    has_in_gifts = False
    has_in_wishes = False

    # 取书籍详情数据
    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)
    book = BookViewBodel(yushu_book.first)

    if current_user.is_authenticated:
        if Gift.query.filter_by(uid = current_user.id, isbn=isbn,launched=False).first():
            has_in_gifts = True
        if Wish.query.filter_by(uid = current_user.id, isbn=isbn,launched=False).first():
            has_in_wishes = True

    # 书籍的交易视图
    trade_gifts = Gift.query.filter_by(isbn=isbn,launched=False).all()
    trade_wishs = Wish.query.filter_by(isbn=isbn,launched=False).all()

    trade_gifts_model = TradeInfo(trade_gifts)
    trade_wishs_model = TradeInfo(trade_wishs)


    return render_template('book_detail.html', book=book, wishes=trade_wishs_model, gifts=trade_gifts_model)
