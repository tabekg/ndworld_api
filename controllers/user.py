from models.candidate import Candidate
from models.user import User


def create_user(db, role, contact_phone_number=None):
    user = User()

    db.add(user)
    db.flush()

    if role == 'candidate':
        candidate = Candidate(
            user_id=user.id,
            contact_phone_number=contact_phone_number,
        )
        db.add(candidate)
        db.flush()

    return user
