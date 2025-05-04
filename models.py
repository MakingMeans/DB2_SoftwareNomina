from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class AppUser(db.Model):
    __tablename__ = 'app_user'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    document_number = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)

class Department(db.Model):
    department_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class EmployeePosition(db.Model):
    __tablename__ = 'employee_position'
    position_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Employee(db.Model):
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
    hire_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    base_salary = db.Column(db.Numeric(12,2), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    position_id = db.Column(db.Integer, db.ForeignKey('employee_position.position_id'))
    department_id = db.Column(db.Integer, db.ForeignKey('department.department_id'))

class PayrollConcept(db.Model):
    __tablename__ = 'payroll_concept'
    concept_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    concept_type = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(100))
    percentage = db.Column(db.Numeric(5,2))
    fixed_value = db.Column(db.Numeric(15,2))

class PayrollType(db.Model):
    __tablename__ = 'payroll_type'
    payroll_type_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)

class PayrollPeriod(db.Model):
    __tablename__ = 'payroll_period'
    payroll_period_id = db.Column(db.Integer, primary_key=True)
    payroll_type_id = db.Column(db.Integer, db.ForeignKey('payroll_type.payroll_type_id'))
    payroll_date = db.Column(db.Date, nullable=False)

class Payroll(db.Model):
    __tablename__ = 'payroll'
    payroll_id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'))
    payroll_period_id = db.Column(db.Integer, db.ForeignKey('payroll_period.payroll_period_id'))
    liquidation_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    worked_days = db.Column(db.Integer, nullable=False)
    total_earnings = db.Column(db.Numeric(12,2), default=0)
    total_deductions = db.Column(db.Numeric(12,2), default=0)
    total_to_pay = db.Column(db.Numeric(12,2), default=0)
    overtime_day_hours = db.Column(db.Numeric(3,1), default=0)
    overtime_night_hours = db.Column(db.Numeric(3,1), default=0)
    overtime_sunday_hours = db.Column(db.Numeric(3,1), default=0)
    overtime_holiday_hours = db.Column(db.Numeric(3,1), default=0)

class PayrollDetail(db.Model):
    __tablename__ = 'payroll_detail'
    detail_id = db.Column(db.Integer, primary_key=True)
    payroll_id = db.Column(db.Integer, db.ForeignKey('payroll.payroll_id'))
    concept_id = db.Column(db.Integer, db.ForeignKey('payroll_concept.concept_id'))
    value = db.Column(db.Numeric(12,2), nullable=False)

class Audit(db.Model):
    __tablename__ = 'audit'
    audit_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('app_user.user_id'))
    description = db.Column(db.String(50), nullable=False)
    affected_table = db.Column(db.String(50), nullable=False)
    action_date = db.Column(db.DateTime, default=db.func.current_timestamp())
