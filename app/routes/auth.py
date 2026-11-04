from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.extensions import db
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

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

        # Find user by email
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):

            # Generate JWT token
            access_token = create_access_token(
                identity=str(user.user_id)
            )

            flash('Login successful!', 'success')

            return redirect(url_for('auth.login'))

        else:
            flash('Invalid email or password!', 'danger')

    return render_template('auth/login.html')