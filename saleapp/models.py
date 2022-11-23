# import data type
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum

from sqlalchemy.orm import relationship

from saleapp import db, app

from datetime import datetime

from enum import Enum as UserEnum

#import UserMixin tử flask_login để quản lý User
from flask_login import UserMixin




# tạo 1 class đối tượng nguồn sử dụng cho các thuộc tính dùng chung, và đc kế thừa từ class Model của db
class BaseModel(db.Model):
    __abstract__ = True  # Giúp không cho tạo table đến mysql
    id = Column(Integer, primary_key=True, autoincrement=True)  # id kiểu số nguyên khóa chính, tự động tăng

# Tạo class Enum phân quyền
class UserRole(UserEnum):
    ADMIN = 1
    USER = 2


# Tạo user quản lý tài khoảng account

# Kế thừa BaseModel, UserMixin (tức đa kế thừa)
class User(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100))
    email = Column(String(50))
    active = Column(Boolean, default=True)
    joined_date = Column(DateTime, default=datetime.now())
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    receipts = relationship('Receipt',backref='user',lazy=True)
    comments = relationship('Comment',backref='user',lazy=True)
    def __str__(self):
        return self.name


# ============ Many To One giữa Category và Product=============





# tạo 1 class đối tượng, kế thừa từ class BaseModel
class Category(BaseModel):
    # chỉ định dạng tên table trong database mysql
    __tablename__ = 'category'
    name = Column(String(20), nullable=False)  # name kiểu String độ dài tối đa 20 ký tự, không được phép null
    # Từ 1 category sẽ có nhiều product
    products = relationship('Product', backref='category', lazy=False)

    # override to string, lấy theo name
    def __str__(self):
        return self.name


# tạo 1 class đối tượng, kế thừa từ class BaseModel
class Product(BaseModel):
    # chỉ định dạng tên table trong database mysql
    __tablename__ = 'product'
    name = Column(String(100), nullable=False)  # name kiểu String độ dài tối đa 20 ký tự, không được phép null
    description = Column(String(255))  # description kiểu String độ dài tối đa 255 ký tự, được phép null
    price = Column(Float, default=0)  # price kiểu Float, mặc định cho bằng 0
    image = Column(String(255))  # image kiểu String độ dài tối đa 100 ký tự, được phép null
    active = Column(Boolean, default=True)  # active kiểu luận lý, bật True
    created_date = Column(DateTime, default=datetime.now())  # created_date kiểu Datetime, mặc định lấy ngày hiện hành
    # thiết lập khóa ngoại , không được phép null
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)

    receipt_details= relationship('ReceiptDetail',backref='product',lazy=True)
    # override to string, lấy theo name

    comments = relationship('Comment',backref='product',lazy=True)
    def __str__(self):
        return self.name

class Comment(BaseModel):
    content = Column(String(255), nullable=False)
    product_id = Column(Integer,ForeignKey(Product.id),nullable=False)
    user_id = Column(Integer,ForeignKey(User.id),nullable=False)
    created_date = Column(DateTime,default=datetime.now())

    def __str__(self):
        return self.content

class Receipt(BaseModel):
    created_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer,ForeignKey(User.id),nullable=False)
    details = relationship('ReceiptDetail',backref='receipt',lazy=True)
class ReceiptDetail(BaseModel):
    receipt_id = Column(Integer,ForeignKey(Receipt.id),nullable=False,primary_key=True)
    product_id = Column(Integer,ForeignKey(Product.id),nullable=False,primary_key=True)

    quantity = Column(Integer,default=0)
    unit_price = Column(Float,default=0)
# thực thi tạo các bảng dữ liệu từ class đã khai báo bên trên
# Khi run thì chương trình sẽ bắt đầu tạo ánh xạ xuống database để kết nối
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # cate1 = Category(name="Smart Phone")
        # cate2 = Category(name="Clock")
        # cate3 = Category(name="Laptop")
        #cate4 = Category(name="Headphone")
        # db.session.add(cate1)
        # db.session.add(cate2)
        # db.session.add(cate3)
        #db.session.add(cate4)

        #db.session.commit()

        # products = [
        #     {
        #         "id": 1,
        #         "name": "Samsung Galaxy Ultra S22",
        #         "description": "Explore and download for free tons of high quality Bmw wallpapers and backgrounds! Customize your desktop, mobile phone and tablet with our wide variety of cool and interesting Bmw wallpapers and Bmw backgrounds in just a few clicks.",
        #         "price": 25500000,
        #         "image": "img/samsung-galaxy-ultra-s22.jpg",
        #         "category_id": 1
        #     },
        #     {
        #         "id": 2,
        #         "name": "Clock Pro A2",
        #         "description": "Explore and download for free tons of high quality Bmw wallpapers and backgrounds! Customize your desktop, mobile phone and tablet with our wide variety of cool and interesting Bmw wallpapers and Bmw backgrounds in just a few clicks.",
        #         "price": 35500000,
        #         "image": "img/wbf36t03713.000-bi5072.01a-dong-ho-nam-day-da-chong-nuoc-citizen.jpg",
        #         "category_id": 2
        #     },
        #     {
        #         "id": 3,
        #         "name": "Rum Pro A3",
        #         "description": "Explore and download for free tons of high quality Bmw wallpapers and backgrounds! Customize your desktop, mobile phone and tablet with our wide variety of cool and interesting Bmw wallpapers and Bmw backgrounds in just a few clicks.",
        #         "price": 30000000,
        #         "image": "img/NP1023-17L_Desktop_2.jpg",
        #         "category_id": 2
        #     },
        #     {
        #         "id": 4,
        #         "name": "Macbook Pro A4",
        #         "description": "Explore and download for free tons of high quality Bmw wallpapers and backgrounds! Customize your desktop, mobile phone and tablet with our wide variety of cool and interesting Bmw wallpapers and Bmw backgrounds in just a few clicks.",
        #         "price": 75000000,
        #         "image": "img/macbook-pro-16-inch-space-gray-m1-pro.jpg",
        #         "category_id": 3
        #     },
        #     {
        #         "id": 5,
        #         "name": "Iphone 14 Pro Max",
        #         "description": "Explore and download for free tons of high quality Bmw wallpapers and backgrounds! Customize your desktop, mobile phone and tablet with our wide variety of cool and interesting Bmw wallpapers and Bmw backgrounds in just a few clicks.",
        #         "price": 36800000,
        #         "image": "img/iphone-14-pro-finish-select-202209-6-7inch-gold.jpg",
        #         "category_id": 1
        #     }
        # ]
        #
        # for p in products:
        #     pro = Product(name=p['name'], price=p['price'], image=p['image'], description=p['description'],
        #                   category_id=p['category_id'])
        #     db.session.add(pro)
        #
        # db.session.commit()
