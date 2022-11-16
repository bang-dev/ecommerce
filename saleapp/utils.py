# Thư viện dùng đọc tập tin json
import json
import os

from saleapp import app

from saleapp.models import Category, Product


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
def load_products(cate_id=None, kw=None, from_price=None, to_price=None):
    products = Product.query.filter(Product.active.__eq__(True))

    if cate_id:
        products = products.filter(Product.category_id.__eq__(cate_id))
    if kw:
        products = products.filter(Product.name.contains(kw))
    if from_price:
        products = products.filter(Product.price.__ge__(from_price))
    if to_price:
        products = products.filter(Product.price.__le__(to_price))
    return products.all()

# def get_product_by_id(product_id):
#     products = read_file_json(os.path.join(app.root_path, 'data/products.json'))
#     for p in products:
#         if p['id'] == product_id:
#             return p
#     return None  # None is NULL in python
def get_product_by_id(product_id):
    return Product.query.get(product_id)
