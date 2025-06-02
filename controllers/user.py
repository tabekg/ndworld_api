from models.user import User, Role


def create_user(db):
    user = User()

    db.add(user)
    db.flush()

    return user


def create_role(db, user_id, agency_id):
    role = Role(
        user_id=user_id,
        agency_id=agency_id,
    )

    db.add(role)
    db.flush()

    return role
