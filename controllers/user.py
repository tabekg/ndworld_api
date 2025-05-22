from models.user import User


def create_user(db):
    user = User()

    db.add(user)
    db.flush()

    return user
