
# app = Flask(__name__)
# app.config.from_object('config')

# @app.route("/hello")
# def hello_world():
#     return "<p>Hello, World</p>"

# 使用make response创建对象
# @app.route("/hello")
# def hello_world():
#     headers = {
#         # 'content-type': 'application/json'
#         # 'content-type': 'text/html'
#         'content-type': 'text/plain'
#     }
#     response = make_response('<html></html>', 200)
#     response.headers = headers
#     return response

# # 返回元组的形式
# @app.route("/hello")
# def hello_world():
#     headers = {
#         # 'content-type': 'application/json'
#         # 'content-type': 'text/html'
#         'content-type': 'text/plain'
#     }
#     return '<html></html>', 200, headers

# @app.run("/book/search/<q>/<page>")
# def search(q, page):
#     """
#        q:普通关键字 isbn
#     """
#     isbn_or_key = util.is_isbn_or_key(q)
#     if isbn_or_key:
#         result  = YuShuBook.search_by_isbn(q)
#     else:
#         result  = YuShuBook.search_by_keywod(q)
#     return jsonify(result)


#第二种路由方式
# app.add_url_rule("/hello", view_func=hello_world)
from app import creare_app


app = creare_app()
if __name__ == "__main__":
    app.run(host = '0.0.0.0', debug=app.config['DEBUG'], threaded=True)
    print(app.url_map)