import time
from apps import db
from .db_users import Users


def seed_users():

    # Cegah duplicate
    if Users.query.first():
        return

    timestamp=int(round(time.time()*1000))
    admin = Users(
        username="Administrator",
        email="administrator@email.com",
        password="Administrator",
        role=0,
        is_active=1,
        created_at=timestamp,
        updated_at=timestamp
    )

    db.session.add(admin)
    db.session.commit()

    return admin