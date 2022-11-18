# Thư viện dùng đọc tập tin json
import json
import os

from saleapp import app, db

from saleapp.models import Category, Product, User

import hashlib #băm password


# Đọc cho global
def read_file_json(path):
    with open(path, "r") as f:  # mở tập tin
        return json.load(f)


# Đọc simple
# def load_categories():
#     return read_file_json(os.path.join(app.root_path, 'data/categories.json'))
def load_categories():
    return Category.query.all()


# Load sản phẩm theo category id
# def load_products(cate_id=None, kw=None, from_price=None, to_price=None):
#     products = read_file_json(os.path.join(app.root_path, 'data/products.json'))
#     if cate_id:
#         products = [p for p in products if p['category_id'] == cate_id]
#     if kw:
#         products = [p for p in products if p['name'].lower().find(kw.lower()) >= 0]
#     if from_price:
#         products = [p for p in products if p['price'] >= float(from_price)]
#     if to_price:
#         products = [p for p in products if p['price'] <= float(to_price)]
#
#     return products
def load_products(cate_id=None, kw=None, from_price=None, to_price=None, page=1):
    products = Product.query.filter(Product.active.__eq__(True))

    if cate_id:
        products = products.filter(Product.category_id.__eq__(cate_id))
    if kw:
        products = products.filter(Product.name.contains(kw))
    if from_price:
        products = products.filter(Product.price.__ge__(from_price))
    if to_price:
        products = products.filter(Product.price.__le__(to_price))
    page_size = app.config['PAGE_SIZE']  # Số lượng sản phẩm tối đa hiển thị trên 1 page
    start = (page - 1) * page_size  # Vị trí bắt đầu
    end = start + page_size  # tới vị trí kết thúc

    # return products.all()
    # in mysql: select * from limit 4 offset 0
    return products.slice(start, end).all()


# def get_product_by_id(product_id):
#     products = read_file_json(os.path.join(app.root_path, 'data/products.json'))
#     for p in products:
#         if p['id'] == product_id:
#             return p
#     return None  # None is NULL in python
def get_product_by_id(product_id):
    return Product.query.get(product_id)



# Đếm số lượng sản phẩm với filter
def count_products():
    # select count * from Product
    return Product.query.filter(Product.active.__eq__(True)).count()


# create new object
def add_user(name, username,password, **kwargs):
    password = str(hashlib.md5(password.strip().encode('utf8')).hexdigest())

    user = User(name=name.strip(),username=username.strip(),password=password,email=kwargs.get('email'), avatar=kwargs.get('avatar'))

    db.session.add(user)
    db.session.commit()

def check_login(username, password):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
        return User.query.filter(User.username.__eq__(username.strip()), User.password.__eq__(password)).first()


def get_user_by_id(user_id):
    return User.query.get(user_id)