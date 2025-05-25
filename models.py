from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum, Numeric, DateTime, Date, func

db = SQLAlchemy()

class AppUser(db.Model):
    __tablename__ = 'app_user'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    document_number = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)

    audits = db.relationship('Audit', backref='user')

class Department(db.Model):
    __tablename__ = 'department'
    department_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    employees = db.relationship('Employee', backref='department')

class EmployeePosition(db.Model):
    __tablename__ = 'employee_position'
    position_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    employees = db.relationship('Employee', backref='position')

class Employee(db.Model):
    __tablename__ = 'employee'
    employee_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    document_type = db.Column(db.String(20), nullable=False)
    document_number = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(100))
    city = db.Column(db.String(100))
    health_insurance = db.Column(db.String(100))
    pension_fund = db.Column(db.String(100))
    hire_date = db.Column(DateTime, default=func.current_timestamp())
    base_salary = db.Column(Numeric(12, 2), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    position_id = db.Column(db.Integer, db.ForeignKey('employee_position.position_id'))
    department_id = db.Column(db.Integer, db.ForeignKey('department.department_id'))

    payrolls = db.relationship('Payroll', backref='employee')

class PayrollConcept(db.Model):
    __tablename__ = 'payroll_concept'
    concept_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    concept_type = db.Column(Enum('earning', 'deduction', 'parafiscal', name='concept_type_enum'), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    percentage = db.Column(Numeric(5, 2))
    fixed_value = db.Column(Numeric(15, 2))

    details = db.relationship('PayrollDetail', backref='concept')

class PayrollType(db.Model):
    __tablename__ = 'payroll_type'
    payroll_type_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(
        Enum('quincenal', 'mensual', 'primas', 'horas extras', 'pagos al empleador', 'vacaciones', name='payroll_type_enum'),
        nullable=False)

    periods = db.relationship('PayrollPeriod', backref='type')

class PayrollPeriod(db.Model):
    __tablename__ = 'payroll_period'
    payroll_period_id = db.Column(db.Integer, primary_key=True)
    payroll_type_id = db.Column(db.Integer, db.ForeignKey('payroll_type.payroll_type_id'))
    payroll_date = db.Column(Date, nullable=False)

    payrolls = db.relationship('Payroll', backref='period')

class Payroll(db.Model):
    __tablename__ = 'payroll'
    payroll_id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'))
    payroll_period_id = db.Column(db.Integer, db.ForeignKey('payroll_period.payroll_period_id'))
    liquidation_date = db.Column(DateTime, default=func.current_timestamp())
    worked_days = db.Column(db.Integer, default=0)
    semester_worked_days = db.Column(db.Integer, default=0)
    total_earnings = db.Column(Numeric(12, 2), default=0)
    total_deductions = db.Column(Numeric(12, 2), default=0)
    total_parafiscal = db.Column(Numeric(12, 2), default=0)
    total_to_pay = db.Column(Numeric(12, 2), default=0)
    overtime_day_hours = db.Column(Numeric(3, 1), default=0)
    overtime_night_hours = db.Column(Numeric(3, 1), default=0)
    overtime_sunday_hours = db.Column(Numeric(3, 1), default=0)
    overtime_holiday_hours = db.Column(Numeric(3, 1), default=0)

    details = db.relationship('PayrollDetail', backref='payroll')

class PayrollDetail(db.Model):
    __tablename__ = 'payroll_detail'
    detail_id = db.Column(db.Integer, primary_key=True)
    payroll_id = db.Column(db.Integer, db.ForeignKey('payroll.payroll_id'))
    concept_id = db.Column(db.Integer, db.ForeignKey('payroll_concept.concept_id'))
    value = db.Column(Numeric(12, 2), nullable=False, default=0)
