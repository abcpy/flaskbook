from app.libs.enums import PendingStatus
from app.web.drift import pending
from . import web
from flask_login import login_required, current_user
from app.models.gift import Gift
from app.models.base import db
from flask import current_app, flash, redirect, url_for, render_template
from app.view_models.gifts import MyGifts
from app.view_models.trade import MyTrade
from app.models.drift import Drift

@web.route("/my/gifts")
@login_required
def my_gifts():
    my_gifts=Gift.my_gifts(uid=current_user.id) 
    isbn_list = [ gift.isbn for gift in my_gifts]
    wishes_count = Gift.get_wish_counts(isbn_list)
    # mygifts = MyGifts(my_gifts, wishes_count)
    mygifts = MyTrade(my_gifts, wishes_count)
    # print("wishes_count", wishes_count)
    #wishes_count [{'count': 1, 'isbn': '9787108070371'}]
    #wishes_count [(1, '9787108070371')]
    #isbn_list ['9787108070371']
    # my_gifts [<Gift 1>]
    return render_template("my_gifts.html",gifts=mygifts.trades)

"""
current_user
"""
@web.route("/gifts/book/<isbn>")
@login_required
def save_to_gifts(isbn):
    if current_user.can_save_to_list(isbn):
        # 事务
        # rollback
        with db.auto_commit():
            print('-----------')
            gift = Gift()
            gift.isbn = isbn
            gift.uid = current_user.id
            current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']
            db.session.add(gift)
        #     db.session.commit()
        # except Exception as e:
        #     db.session.rollback()
        #     raise e
    else:
        flash('这本书已添加至你的赠送清单或已存在你的心愿清单, 请不要重复添加')
    return redirect(url_for("web.book_detail", isbn=isbn))

@web.route("/gifts/<gid>/redraw")
@login_required
def redraw_from_gifts(gid):
        drift = Drift.query.filter_by(gifter_id=gid, pending=PendingStatus.Waiting).first()
        gift = Gift.query.filter_by(id=gid,launched=False,uid=current_user.id).first_or_404()

        if drift:
            flash("正处于交易状态，不可删除")
        else:
            with db.auto_commit():
                gift.delete()
        return redirect(url_for('web.my_gifts'))