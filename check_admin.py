from flask import Flask
from models import db, Admin

# Check SQLite
sqlite_app = Flask(__name__)
sqlite_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///c:/Users/aksha/OneDrive/Desktop/qr_attendance_system/instance/qr_attendance.db'
db.init_app(sqlite_app)

with sqlite_app.app_context():
    admins = Admin.query.all()
    print('SQLite Admins:', [(a.username, a.password_hash[:20] + '...') for a in admins])

# Check MySQL
mysql_app = Flask(__name__)
mysql_app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:akshata18@localhost:3306/qr_attendance'
mysql_db = db  # reuse
db.init_app(mysql_app)

with mysql_app.app_context():
    admins = Admin.query.all()
    print('MySQL Admins:', [(a.username, a.password_hash[:20] + '...') for a in admins])