from flask import redirect

from saleapp import app, db
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView

from saleapp.models import Category, Product, UserRole
from flask_login import current_user, logout_user

admin = Admin(app=app, name="E-commerce Administration", template_mode='bootstrap4')


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.ADMIN)


class ProductView(ModelView):
    column_display_pk = True  # Hiển thị khóa chính sản phẩm
    can_view_details = True  # Display view
    can_export = True  # # Display export
    column_searchable_list = ['name', 'description']  # Display search
    column_filters = ['name', 'price']  # Display filters

    # Loại bỏ 1 field hiển thị, vd: Không lấy cột image
    column_exclude_list = ['image']

    # Đổi tên column
    column_labels = {
        'id': 'Mã sản phẩm',
        'name': 'Tên sản phẩm',
        'description': 'Mô tả',
        'price': 'Giá bán',
        'image': 'Ảnh đại diện',
        'category': 'Danh mục',
        'active': 'Hoạt động',
        'created_date': 'Ngày tạo'

    }

    column_sortable_list = ['id', 'name', 'price']  # Sắp xếp


class LogoutView(BaseView):
    @expose('/')
    def home_admin_page(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


# admin.add_view(ModelView(Category, db.session))
admin.add_view(AuthenticatedModelView(Category, db.session))

# admin.add_view(ModelView(Product, db.session))
#admin.add_view(ProductView(Product, db.session))  # Xem chi tiết sản phẩm
admin.add_view(AuthenticatedModelView(Product, db.session))

admin.add_view(LogoutView(name="Logout"))
