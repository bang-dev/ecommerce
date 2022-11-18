from saleapp import app, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from saleapp.models import Category, Product

admin = Admin(app=app, name="E-commerce Administration", template_mode='bootstrap4')

class ProductView(ModelView):
    column_display_pk = True #Hiển thị khóa chính sản phẩm
    can_view_details = True # Display view
    can_export = True # # Display export
    column_searchable_list = ['name','description'] # Display search
    column_filters = ['name','price'] # Display filters

    #Loại bỏ 1 field hiển thị, vd: Không lấy cột image
    column_exclude_list = ['image']

    #Đổi tên column
    column_labels = {
        'id':'Mã sản phẩm',
        'name': 'Tên sản phẩm',
        'description':'Mô tả',
        'price':'Giá bán',
        'image':'Ảnh đại diện',
        'category':'Danh mục',
        'active': 'Hoạt động',
        'created_date':'Ngày tạo'

    }

    column_sortable_list = ['id','name','price'] # Sắp xếp


admin.add_view(ModelView(Category, db.session))
#admin.add_view(ModelView(Product, db.session))
admin.add_view(ProductView(Product,db.session)) # Xem chi tiết sản phẩm
