from flask import Blueprint, get_flashed_messages, render_template, request, redirect, url_for, flash
from app.extensions import db
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from flask_jwt_extended import (
    create_access_token,
    set_access_cookies,
    jwt_required,
    get_jwt_identity
)
from flask_jwt_extended import (
    create_access_token,
    set_access_cookies,
    jwt_required,
    get_jwt_identity,
    get_jwt,
    unset_jwt_cookies
)
from app.models import User, DamageReport
from datetime import datetime
from decimal import Decimal, InvalidOperation

auth = Blueprint('auth', __name__)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':

        full_name = request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')
        phone = request.form.get('phone')
        district = request.form.get('district')

        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash('Email already registered!', 'danger')
            return redirect(url_for('auth.signup'))

        # Hash password
        hashed_password = generate_password_hash(password)

        # Create new citizen
        new_user = User(
            full_name=full_name,
            email=email,
            password=hashed_password,
            phone=phone,
            district=district,
            role='citizen'
        )

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/signup.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form.get('email').strip().lower()
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):

            access_token = create_access_token(
                identity=str(user.user_id)
            )

            flash('Login successful!', 'success')
            
            if user.role == 'citizen':
                dashboard_url = url_for('auth.dashboard')
            elif user.role == 'officer':
                dashboard_url = url_for('auth.officer_dashboard')
            elif user.role == 'admin':
                dashboard_url = url_for('auth.admin_dashboard')
            else:
                flash('Invalid user role!', 'danger')
                return redirect(url_for('auth.login'))
            response = redirect(dashboard_url)
            
            set_access_cookies(response, access_token)

            return response

        else:
            flash('Invalid email or password!', 'danger')

    return render_template('auth/login.html')

@auth.route('/dashboard')
@jwt_required()
def dashboard():

    user_id = get_jwt_identity()

    user = User.query.get_or_404(int(user_id))

    return render_template(
        'citizen/dashboard.html',
        user=user,
        csrf_token=get_jwt()["csrf"]
    )
    
@auth.route('/officer/dashboard')
@jwt_required()
def officer_dashboard():

    user_id = get_jwt_identity()
    user = User.query.get_or_404(int(user_id))

    if user.role != 'officer':
        return "Access Denied", 403

    return render_template(
    'officer/dashboard.html',
    user=user,
    csrf_token=get_jwt()['csrf']
)


@auth.route('/admin/dashboard')
@jwt_required()
def admin_dashboard():

    user_id = get_jwt_identity()
    user = User.query.get_or_404(int(user_id))

    if user.role != 'admin':
        return "Access Denied", 403
    
    # Clear old flash messages
    get_flashed_messages()
    
    return render_template(
        'admin/dashboard.html',
        user=user
    )  
    
@auth.route('/admin/create-officer', methods=['GET', 'POST'])
@jwt_required()
def create_officer():

    user_id = get_jwt_identity()
    current_user = User.query.get_or_404(int(user_id))

    # Only Admin can create Officer accounts
    if current_user.role != 'admin':
        return "Access Denied", 403

    if request.method == 'POST':

        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not full_name or not email or not password:
            flash('All fields are required!', 'danger')

        elif len(password) < 8:
            flash('Password must contain at least 8 characters!', 'danger')

        elif password != confirm_password:
            flash('Passwords do not match!', 'danger')

        elif User.query.filter_by(email=email).first():
            flash('Email already registered!', 'danger')

        else:
            new_officer = User(
                full_name=full_name,
                email=email,
                password=generate_password_hash(password),
                role='officer'
            )

            db.session.add(new_officer)
            db.session.commit()

            flash('Officer account created successfully!', 'success')

            return redirect(url_for('auth.create_officer'))

    return render_template(
        'admin/create_officer.html',
        csrf_token=get_jwt()['csrf']
    ) 
    
@auth.route('/logout', methods=['POST'])
@jwt_required()
def logout():

    # Clear previously stored flash messages
    get_flashed_messages()

    response = redirect(url_for('auth.login'))

    unset_jwt_cookies(response)

    flash('You have successfully logged out!', 'success')

    return response 

@auth.route('/citizen/report-damage', methods=['GET', 'POST'])
@jwt_required()
def report_damage():

    user_id = get_jwt_identity()
    user = User.query.get_or_404(int(user_id))

    if user.role != 'citizen':
        return "Access Denied", 403

    if request.method == 'POST':

        damage_type = request.form.get('damage_type', '').strip()
        incident_date = request.form.get('incident_date', '')
        location = request.form.get('location', '').strip()
        estimated_loss = request.form.get('estimated_loss', '0').strip()
        description = request.form.get('description', '').strip()

        if not damage_type or not incident_date or not location:
            flash('Please fill in all required fields!', 'danger')

        else:
            try:
                incident_date = datetime.strptime(
                    incident_date, '%Y-%m-%d'
                ).date()

                estimated_loss = Decimal(estimated_loss)

                if estimated_loss < 0:
                    raise ValueError

                report = DamageReport(
                    user_id=user.user_id,
                    damage_type=damage_type,
                    incident_date=incident_date,
                    location=location,
                    estimated_loss=estimated_loss,
                    description=description
                )

                db.session.add(report)
                db.session.commit()

                flash('Damage report submitted successfully!', 'success')
                return redirect(url_for('auth.report_damage'))

            except (ValueError, InvalidOperation):
                flash('Please enter valid date and damage amount!', 'danger')

    return render_template(
        'citizen/report_damage.html',
        user=user,
        csrf_token=get_jwt()['csrf']
    )
    
@auth.route('/citizen/my-reports')
@jwt_required()
def my_reports():

    user_id = get_jwt_identity()
    user = User.query.get_or_404(int(user_id))

    if user.role != 'citizen':
        return "Access Denied", 403

    reports = DamageReport.query.filter_by(
        user_id=user.user_id
    ).order_by(
        DamageReport.created_at.desc()
    ).all()

    return render_template(
        'citizen/my_reports.html',
        user=user,
        reports=reports
    )    