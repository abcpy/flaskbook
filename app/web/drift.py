from app.models.wish import Wish
from sqlalchemy import or_, desc
import re
from flask_login.utils import login_required
from . import web
from app.models.gift import Gift
from flask_login import current_user
from flask import flash, render_template, redirect, url_for, request
from app.forms.book import DriftForm
from app import db
from app.view_models.book import BookViewBodel
from app.libs.email import semd_mail
from app.models.drift import Drift
from app.view_models.drift import DriftCollection
from app.libs.enums import PendingStatus

@web.route("/drift/<int:gid>", methods=['GET', 'POST'])
@login_required
def send_drift(gid):
    # 1. 通过gid找到找到Gid对象
    current_gift =  Gift.query.get_or_404(gid)
    # 2. 判断这本书是否是要出人自己的
    if current_gift.is_yourself_gift(current_user.id):
        flash("这边书是你自己的， 不能向自己要书籍")
        return redirect(url_for('web.book_detail', isbn=current_gift.isbn))
    # 3. 是否有足够的币
    can = current_user.can_satisfied_with()
    if not can:
        return render_template('not_enough_beans.html', beans=current_user.beans)
    gifter = current_gift.user.summary
    form = DriftForm(request.form)
    if request.method == 'POST' and form.validate():
        with db.auto_commit():
            drift = Drift()
            # drift.message = form.message.data
            # drift.recipient_name = form.recipient_name.data
            # drift.mobile = form.mobile.data
            # drift.address = form.address.data
            form.populate_obj(drift)
            drift.gift_id = current_gift.id
            drift.requestr_id = current_user.id
            drift.requester_nicname = current_user.nickname
            drift.gifter_nickname = current_gift.user.nickname
            drift.gifter_id = current_gift.user.id
            
            book = BookViewBodel(current_gift.book)

            drift.book_title = book.title
            drift.book_author = book.author
            drift.book_img = None
            drift.isbn = book.isbn
            db.session.add(drift)
        semd_mail(current_gift.user.email, '有人想要一本书','email/get_gift.html',wisher=current_user,gift=current_gift)
        return redirect(url_for('web.pending'))

    return render_template('drift.html', gifter=gifter, user_beans=current_user.beans,form=form)

"""
   我作为索要者的交易
   我作为赠送者的交易
   时间倒序排序
"""
@web.route("/pending")
@login_required
def pending():
    drifts = db.session.query(Drift).filter(
        or_(Drift.gifter_id==current_user.id, Drift.requestr_id==current_user.id)).order_by(
            desc(Drift.create_time)).all()
    driftcollection = DriftCollection(drifts, current_user.id)
    return render_template('pending.html', drifts = driftcollection.data)

@web.route("/drift/<int:did>/reject")
@login_required
def reject_drift(did):
    with db.auto_commit():
        drift = db.session.query().filter(Gift.uid==current_user.id, Drift.id == did).first_or_404()
        drift.pending = PendingStatus.Reject
    return redirect(url_for('web.pending'))


@web.route("/drift/<int:did>/redraw")
@login_required
def redraw_drift(did):
    # 超权
    with db.auto_commit():
        drift = Drift.query.filter_by(requestr_id=current_user.id, id=did).first_or_404()
        drift.pending = PendingStatus.Redraw
    return redirect(url_for('web.pending'))
    # print(drift.pending)
    # PendingStatus.Waiting

@web.route("/drift/<int:did>/mailed")
@login_required
def mailed_drift(did):
    with db.auto_commit():
        drift = Drift.query.filter_by(id=did, gifter_id=current_user.id).first_or_404()
        drift.pending = PendingStatus.Success

        gift = Gift.query.filter_by(id=drift.gift_id).first_or_404()
        gift.launched = True

        wish = Wish.query.filter_by(uid=drift.requestr_id, isbn=drift.isbn).first_or_404()
        wish.launched = True
    return redirect(url_for('web.pending'))
