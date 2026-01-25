import getpass
from app import create_app
from app.extensions import db
from app.models.user import User

def main():
    app = create_app()
    with app.app_context():
        email = input("Admin email: ").strip().lower()
        full_name = input("Full name: ").strip()
        phone = input("Phone (optional): ").strip() or None
        password = getpass.getpass("Password: ")

        existing = User.query.filter_by(email=email).first()
        if existing:
            existing.role = "admin"
            if full_name:
                existing.full_name = full_name
            existing.phone = phone
            if password:
                existing.set_password(password)
            db.session.commit()
            print("Updated existing user to admin ✅")
            return

        admin = User(email=email, full_name=full_name, phone=phone, role="admin")
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
        print("Admin created ✅")

if __name__ == "__main__":
    main()
