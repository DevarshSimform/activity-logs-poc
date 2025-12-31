from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.database.models import User
from app.core.config import settings
from app.core.security import JWTService

def create_admin_user():
    db: Session = SessionLocal()
    jwt_service = JWTService()

    try:
        admin_email = settings.admin_email
        admin_password = settings.admin_password

        if not admin_email or not admin_password:
            print("⚠️ Admin credentials not found in .env")
            return

        existing_admin = (
            db.query(User)
            .filter(User.email == admin_email)
            .first()
        )

        if existing_admin:
            print("ℹ️ Admin user already exists")
            return

        admin = User(
            email=admin_email,
            firstname="System",
            lastname="Admin",
            hashed_password=jwt_service.hash_password(admin_password),
            is_admin=True,
        )

        db.add(admin)
        db.commit()

        print(f"✅ Admin user created: {admin_email}")

    except Exception as e:
        db.rollback()
        print("❌ Failed to create admin user:", str(e))

    finally:
        db.close()
