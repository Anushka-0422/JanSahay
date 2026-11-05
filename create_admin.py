from getpass import getpass

from app import create_app
from app.extensions import db
from app.models import User
from werkzeug.security import generate_password_hash


app = create_app()

with app.app_context():

    print("\n===== JanSahay Admin Account Creation =====")

    full_name = input("Enter Admin Name: ").strip()
    email = input("Enter Admin Email: ").strip().lower()
    password = getpass("Enter Admin Password: ")
    confirm_password = getpass("Confirm Admin Password: ")

    if not full_name or not email or not password:
        print("All fields are required.")

    elif password != confirm_password:
        print("Passwords do not match.")

    elif User.query.filter_by(email=email).first():
        print("An account with this email already exists.")

    else:
        admin = User(
            full_name=full_name,
            email=email,
            password=generate_password_hash(password),
            role="admin"
        )

        db.session.add(admin)
        db.session.commit()

        print("\nAdmin account created successfully!")