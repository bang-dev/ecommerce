from flask import Flask

# import sqlalchemy tương tác vs database
from flask_sqlalchemy import SQLAlchemy

# thiết lập cấu hình app
app = Flask(__name__)

# Cấu hình Key chuỗi kết nối
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:abc123@localhost/db_dev_ecommerce?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
# thiết lập cấu hình tương tác database
db = SQLAlchemy(app=app)
