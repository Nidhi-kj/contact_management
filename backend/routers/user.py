from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from main.database import get_db

from schema.user import UserCreate, UserUpdate
from schema.auth import LoginRequest

from CRUD.user import (
    get_users,
    get_user_by_id,
    create_user,
    update_user,
    delete_user
)

from models.user import User

from utils.password import get_password_hash, verify_password
from utils.auth import create_access_token

router = APIRouter()

# Public user response
def user_response(user):
    return {
        "user_id": user.user_id,
        "name": user.name,
        "email": user.email,
        "phone": user.phone
    }


# Get all users
@router.get("/users")
def read_users(db: Session = Depends(get_db)):
    users = get_users(db)
    return [user_response(user) for user in users]


# Get user by ID
@router.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):

    user = get_user_by_id(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user_response(user)


# Register user
@router.post("/users", status_code=status.HTTP_201_CREATED)
def post_users(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = get_password_hash(user.password)

    new_user = create_user(db, user, hashed_password)

    return user_response(new_user)


# Login user
@router.post("/users/login")
def login_user(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == login_data.email
    ).first()

    if user is None or not verify_password(
        login_data.password,
        user.pass_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token = create_access_token(
        data={"sub": str(user.user_id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# Update user
@router.put("/users/{user_id}")
def put_users(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db)
):

    updated_user = update_user(db, user_id, user)

    if updated_user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user_response(updated_user)


# Delete user
@router.delete("/users/{user_id}")
def delete_users(user_id: int, db: Session = Depends(get_db)):

    deleted_user = delete_user(db, user_id)

    if deleted_user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {"message": "User deleted successfully"}
