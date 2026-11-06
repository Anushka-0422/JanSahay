from app.extensions import db
from datetime import datetime


# 1. Users Table
class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(15))
    district = db.Column(db.String(100))
    role = db.Column(db.String(20), nullable=False, default='citizen')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# 2. Damage Reports Table
class DamageReport(db.Model):
    __tablename__ = 'damage_reports'

    report_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    damage_type = db.Column(db.String(100), nullable=False)
    incident_date = db.Column(db.Date, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    estimated_loss = db.Column(db.Numeric(12, 2))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# 3. Schemes Table
class Scheme(db.Model):
    __tablename__ = 'schemes'

    scheme_id = db.Column(db.Integer, primary_key=True)
    scheme_name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    eligibility = db.Column(db.Text)
    required_documents = db.Column(db.Text)
    official_link = db.Column(db.String(255))
    status = db.Column(db.Boolean, default=True)


# 4. Applications Table
class Application(db.Model):
    __tablename__ = 'applications'

    application_id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey('damage_reports.report_id'), nullable=False)
    scheme_id = db.Column(db.Integer, db.ForeignKey('schemes.scheme_id'), nullable=False)
    officer_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    status = db.Column(db.String(30), default='Pending')
    remarks = db.Column(db.Text)
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    report = db.relationship('DamageReport', backref='applications')
    scheme = db.relationship('Scheme', backref='applications')
    officer = db.relationship('User', foreign_keys=[officer_id])