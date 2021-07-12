
from . import web
from flask import render_template
from app.models.gift import Gift
from app.view_models.book import BookViewBodel

@web.route('/')
def index():
    recent_gift = Gift().recent()
    books = [BookViewBodel(gift.book) for gift in recent_gift]
    return render_template("index.html", recent=books)

@web.route('/personal')
def personal_center():
    pass