from datetime import datetime

from flask import redirect, request

from saleapp import app, db
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView

from saleapp.models import Category, Product, UserRole, User
from flask_login import current_user, logout_user

from saleapp.utils import category_statistic, product_statistic, product_month_statistic


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


class UserView(ModelView):
    pass


class LogoutView(BaseView):
    @expose('/')
    def home_admin_page(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


class StatisticsView(BaseView):
    @expose('/')
    def __index__(self):
        kw = request.args.get('kw')
        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')
        year = request.args.get('year', datetime.now().year)
        return self.render('admin/statistics.html', month_statistic_render_web=product_month_statistic(year=year)
                           , statistic_prod_render_web=product_statistic(kw=kw, from_date=from_date, to_date=to_date))

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def __index__(self):
        return self.render('admin/index.html', statistic_cate_render_web=category_statistic())


admin = Admin(app=app, name="E-commerce Administration", template_mode='bootstrap4', index_view=MyAdminIndexView())

# admin.add_view(ModelView(Category, db.session))
admin.add_view(AuthenticatedModelView(Category, db.session))

# admin.add_view(ModelView(Product, db.session))
# admin.add_view(ProductView(Product, db.session))  # Xem chi tiết sản phẩm
admin.add_view(AuthenticatedModelView(Product, db.session))

admin.add_view(LogoutView(name="Logout"))

admin.add_view(AuthenticatedModelView(User, db.session))

admin.add_view(StatisticsView("Statistics"))
