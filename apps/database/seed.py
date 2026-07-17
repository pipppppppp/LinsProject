import time
from apps import db
from .db_users import Users
from apps.utilities.utilities import hash_password

def seed_users():
    admin = Users.query.filter_by(role=0).first()

    if admin:
        return admin
    timestamp=int(round(time.time()*1000))
    hashed_password = hash_password("Administrator")
    admin = Users(
        username="Administrator",
        email="administrator@email.com",
        password=hashed_password,
        role=0,
        is_active=1,
        created_at=timestamp,
        updated_at=timestamp
    )
    db.session.add(admin)
    db.session.commit()

    return admin