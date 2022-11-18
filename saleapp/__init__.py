from flask import Flask

# import sqlalchemy tương tác vs database
from flask_sqlalchemy import SQLAlchemy

# import cloudinary hỗ trợ việc upload lưu trử ảnh và video
import cloudinary

#import LoginManager để quản lý đăng nhập
from flask_login import LoginManager

# thiết lập cấu hình app
app = Flask(__name__)

# Cấu hình Key chuỗi kết nối
app.secret_key = '@#$FGH#$%^&*GH465456EDFGBN#$%^&*J'  # Hỗ trợ việc thêm 1 sản phẩm, do quá trình chuyển trang có sủ dụng session cần có 1 secret_key để mã hóa
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:abc123@localhost/db_dev_ecommerce?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# Cấu hình hiển thị số lượng tối đa mỗi 1 trang page
app.config['PAGE_SIZE'] = 2
# thiết lập cấu hình tương tác database
db = SQLAlchemy(app=app)

# Cấu hình thông tin để kết nối với cloudinary
cloudinary.config(
    cloud_name= 'do20urnhr',
    api_key= '923335259698874',
    api_secret= 'VphL4JPzZYIxEXdAiT8JNyouPuM')
#cấu hình login để quản lý app
login = LoginManager(app=app)