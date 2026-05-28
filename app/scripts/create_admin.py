"""Idempotent admin seed script.

Reads ADMIN_NAME, ADMIN_EMAIL, ADMIN_PASSWORD from the environment
(typically loaded from .env) and creates a single admin user if one
with that email does not already exist.

Run with:
    python -m app.scripts.create_admin
"""

import os
import sys

from dotenv import load_dotenv

from app.database import SessionLocal
from app.services.auth import create_admin_user


def main() -> int:
    load_dotenv()

    name = os.getenv("ADMIN_NAME")
    email = os.getenv("ADMIN_EMAIL")
    password = os.getenv("ADMIN_PASSWORD")

    missing = [
        key
        for key, value in (
            ("ADMIN_NAME", name),
            ("ADMIN_EMAIL", email),
            ("ADMIN_PASSWORD", password),
        )
        if not value
    ]
    if missing:
        print(f"Missing required environment variables: {', '.join(missing)}")
        return 1

    db = SessionLocal()
    try:
        admin = create_admin_user(db, name=name, email=email, password=password)
    finally:
        db.close()

    if admin is None:
        print(f"Admin with email {email} already exists. Nothing to do.")
        return 0

    print(f"Admin created: {admin.email} (id={admin.id})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
