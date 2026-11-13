
from sqlalchemy.orm import Session
from models.user import User


# Get all users
def get_users(db: Session):
    return db.query(User).all()


# Get user by ID
def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(
        User.user_id == user_id
    ).first()


# Create new user
def create_user(db: Session, user_data, password_hash: str):

    new_user = User(
        name=user_data.name,
        email=user_data.email,
        phone=user_data.phone,
        pass_hash=password_hash
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# Update user
def update_user(db: Session, user_id: int, user_data):

    user = db.query(User).filter(
        User.user_id == user_id
    ).first()

    if user is None:
        return None

    update_data = user_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return user


# Delete user
def delete_user(db: Session, user_id: int):

    user = db.query(User).filter(
        User.user_id == user_id
    ).first()

    if user is None:
        return None

    db.delete(user)
    db.commit()

    return user
