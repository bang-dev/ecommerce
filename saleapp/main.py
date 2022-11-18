import math

import cloudinary.uploader
from flask import render_template, request, redirect, url_for
from saleapp import app, login
from saleapp.models import UserRole
# import modules utils để sủ dụng cho module
from utils import load_categories, load_products, get_product_by_id, count_products, add_user, check_login, \
    get_user_by_id
from flask_login import login_user, logout_user


# ================== CONTROLLER ===================
@app.route('/')
def home_page():
    # Đổ danh sách category
    # cates = load_categories()
    kw = request.args.get('keyword')
    cate_id = request.args.get('category_id')

    # Lấy page
    page = request.args.get('page', 1)  # Mặc lấy trang đầu
    # Lấy số lượng sản phẩm
    counter = count_products()
    prods = load_products(cate_id=cate_id, kw=kw, page=int(page))
    # categories_render_web = cates,
    return render_template('index.html',
                           products_render_web=prods,
                           pages_render_web=math.ceil(counter / app.config['PAGE_SIZE']))  # Làm tròn lên số trang


@app.route(
    '/products')  # có thể truyền /products hoặc tên function vào url web, nên dùng (tên function để truyền) {{ url_for('<function_name>')}}
def products_list():
    # truyền category id
    cate_id = request.args.get('category_id')
    # truyền keyword
    kw = request.args.get('keyword')
    # truyền from price , to price
    from_price = request.args.get('from_price')
    to_price = request.args.get('to_price')
    # Đổ danh sách sản phẩm
    pros = load_products(cate_id=cate_id, kw=kw, from_price=from_price, to_price=to_price)
    return render_template('products.html', products_render_web=pros)


@app.route('/products/<product_id>')
def product_detail(product_id):
    product = get_product_by_id(product_id)
    return render_template('product-detail.html', product=product)


# Hổ trợ thêm 2 method GET and POST
# GET : giúp hổ truy cập vào trang sign-in
# POST : hổ trợ để nhấn submit để thực hiện đăng ký
@app.route("/register", methods=['get', 'post'])
def user_register():
    err_msg = ""
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        confirm = request.form.get('confirm')
        avatar_path = None

        try:
            if password.strip().__eq__(confirm.strip()):
                avatar = request.files.get('avatar')

                if avatar:
                    response = cloudinary.uploader.upload(avatar)
                    avatar_path = response['secure_url']
                add_user(name=name, username=username, password=password, email=email, avatar=avatar_path)
                return redirect(url_for('user_login'))
            else:
                err_msg = 'Invalid password and confirm password !!!'
        except Exception as exc:
            err_msg = "System Error !!!" + str(exc)

    return render_template('sign-up.html', err_msg=err_msg)


# do đây dùng phía client nên phải dùng get để lấy thông tin và post thực hiện đăng nhập
@app.route('/user-login', methods=['get', 'post'])
def user_login():
    err_msg = " "
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = check_login(username=username, password=password)
        if user:
            # Ghi nhận trạng thái đăng nhập
            login_user(user=user)
            return redirect(url_for('home_page'))
        else:
            err_msg = 'Username or password invalid !!!'
    return render_template('sign-in.html', err_msg=err_msg)


@app.route('/admin-login',methods=['post'])
def login_admin():
    err_msg = " "
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = check_login(username=username, password=password, role=UserRole.ADMIN)
        if user:
            # Ghi nhận trạng thái đăng nhập
            login_user(user=user)

    return redirect('/admin')

@app.route('/user-logout')
def user_logout():
    logout_user()
    return redirect(url_for('user_login'))


@app.context_processor  # gắn tất cả các response trên hệ thống website
def common_response():
    return {
        'categories_render_web': load_categories()
    }


@login.user_loader
def user_load(user_id):
    return get_user_by_id(user_id=user_id)


if __name__ == '__main__':
    # import trang admin
    from saleapp.admin import *

    app.run(debug=True)
