from models.user import User


def create_user(contact_phone_number=None):
    user = User(
        contact_phone_number=contact_phone_number,
    )

    return user
