from . import web
from flask_login import current_user,login_required
from app import db
from app.models.wish import Wish
from flask import flash, redirect, url_for, render_template
from app.view_models.wishes import myWishes
from app.view_models.trade import MyTrade

@web.route("/my/wish")
@login_required
def my_wish():
    uid = current_user.id
    mywish = Wish.myWishes(uid)
    isbn_list = [ wish.isbn for wish in mywish]
    wishes_count = Wish.get_wishes_count(isbn_list)
    # wishes = myWishes(mywish, wishes_count)
    wishes = MyTrade(mywish, wishes_count)
    # mywishes [{'count': 1, 'isbn': '9787108070371'}]
    # mywishes [(1, '9787108070371')]
    # print("mywishes", wishes_count) 
    # mywishes ['9787108070371']
    # mywishes [<Wish 1>]
    return render_template("my_wish.html", wishes=wishes.trades)


@web.route("/wish/book/<isbn>")
@login_required
def save_to_wish(isbn):
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            wish = Wish()
            wish.isbn = isbn
            wish.uid = current_user.id
            db.session.add(wish)
    else:
         flash("这本书已被加入心愿清单")
    return redirect(url_for("web.book_detail", isbn=isbn))

@web.route("/satisfy/wish/<int:wid>")
def satisfy_wish():
    pass

@web.route("/wish/book/<isbn>/redraw")
@login_required
def redraw_from_wish(isbn):
    wish = Wish.query.filter_by(isbn=isbn,launched=False,uid=current_user.id).first_or_404()
    with db.auto_commit():
        wish.delete()
    return redirect(url_for('web.my_wish'))