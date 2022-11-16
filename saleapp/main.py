from flask import render_template, request
from saleapp import app
# import modules utils để sủ dụng cho module
from utils import load_categories, load_products, get_product_by_id

# ================== CONTROLLER ===================
@app.route('/')
def home_page():
    # Đổ danh sách category
    cates = load_categories()
    kw = request.args.get('keyword')
    cate_id = request.args.get('category_id')
    prods = load_products(cate_id=cate_id,kw=kw)
    return render_template('index.html', categories_render_web=cates, products_render_web=prods)

@app.route('/products')  # có thể truyền /products hoặc tên function vào url web, nên dùng (tên function để truyền) {{ url_for('<function_name>')}}
def products_list():

    # truyền category id
    cate_id = request.args.get('category_id')
    # truyền keyword
    kw = request.args.get('keyword')
    #truyền from price , to price
    from_price=request.args.get('from_price')
    to_price=request.args.get('to_price')
    #Đổ danh sách sản phẩm
    pros = load_products(cate_id=cate_id,kw=kw,from_price=from_price,to_price=to_price)
    return render_template('products.html', products_render_web=pros)


@app.route('/products/<product_id>')
def product_detail(product_id):
    product = get_product_by_id(product_id)
    return render_template('product-detail.html',product=product)





if __name__ == '__main__':
    app.run(debug=True)
