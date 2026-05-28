"""
Promote an existing user to admin privileges.

Run from the project root directory:

docker compose exec api python -m scripts.promote_user user@example.com
"""

import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config.config import settings
from app.models.user import User

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(bind=engine)

def promote_user(email: str):
    db = SessionLocal()


    try:
        user = db.query(User).filter(User.email == email).first()

        if not user:
            print(f"User not found: {email}")
            return

        if user.is_admin:
            print(f"User is already an admin: {email}")
            return

        user.is_admin = True
        db.commit()

        print(f"Successfully promoted user to admin: {email}")

    finally:
        db.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage:")
        print("python scripts/promote_user.py user@example.com")
        sys.exit(1)

    email = sys.argv[1]

    promote_user(email)

