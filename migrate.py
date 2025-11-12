from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db, Employee, Attendance, Admin
import os

# SQLite app
sqlite_app = Flask(__name__)
sqlite_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///c:/Users/aksha/OneDrive/Desktop/qr_attendance_system/instance/qr_attendance.db'
sqlite_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(sqlite_app)

# MySQL app
mysql_app = Flask(__name__)
mysql_app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:akshata18@localhost:3306/qr_attendance'
mysql_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
mysql_db = SQLAlchemy(mysql_app)

# Define models for MySQL
class MySQLEmployee(mysql_db.Model):
    __tablename__ = 'employee'
    id = mysql_db.Column(mysql_db.Integer, primary_key=True)
    name = mysql_db.Column(mysql_db.String(100), nullable=False)
    emp_code = mysql_db.Column(mysql_db.String(20), unique=True, nullable=False)
    qr_data = mysql_db.Column(mysql_db.String(150), unique=True, nullable=False)
    daily_salary = mysql_db.Column(mysql_db.Float, nullable=False, default=500)

class MySQLAttendance(mysql_db.Model):
    __tablename__ = 'attendance'
    id = mysql_db.Column(mysql_db.Integer, primary_key=True)
    emp_code = mysql_db.Column(mysql_db.String(20), nullable=False)
    date = mysql_db.Column(mysql_db.Date, nullable=False)
    time_in = mysql_db.Column(mysql_db.Time, nullable=False)
    time_out = mysql_db.Column(mysql_db.Time)

class MySQLAdmin(mysql_db.Model):
    __tablename__ = 'admin'
    id = mysql_db.Column(mysql_db.Integer, primary_key=True)
    username = mysql_db.Column(mysql_db.String(50), unique=True, nullable=False)
    password_hash = mysql_db.Column(mysql_db.String(256), nullable=False)

def migrate():
    with sqlite_app.app_context():
        # Read from SQLite
        employees = Employee.query.all()
        attendances = Attendance.query.all()
        admins = Admin.query.all()

    with mysql_app.app_context():
        mysql_db.drop_all()
        mysql_db.create_all()

        # Insert employees
        for emp in employees:
            mysql_emp = MySQLEmployee(
                id=emp.id,
                name=emp.name,
                emp_code=emp.emp_code,
                qr_data=emp.qr_data,
                daily_salary=emp.daily_salary
            )
            mysql_db.session.add(mysql_emp)

        # Insert attendances
        for att in attendances:
            mysql_att = MySQLAttendance(
                id=att.id,
                emp_code=att.emp_code,
                date=att.date,
                time_in=att.time_in,
                time_out=att.time_out
            )
            mysql_db.session.add(mysql_att)

        # Insert admins
        for admin in admins:
            mysql_admin = MySQLAdmin(
                id=admin.id,
                username=admin.username,
                password_hash=admin.password_hash
            )
            mysql_db.session.add(mysql_admin)

        mysql_db.session.commit()
        print("Migration completed successfully!")

if __name__ == '__main__':
    migrate()