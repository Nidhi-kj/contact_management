
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from main.database import get_db
from models.user import User
from schema.phone import PhoneCreate, PhoneUpdate
from utils.auth import get_current_user

from CRUD.phone import (
    get_phones,
    get_phone_by_id,
    create_phone,
    update_phone,
    delete_phone
)

router = APIRouter()


@router.get("/phones")
def read_phones(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_phones(db, current_user.user_id)


@router.get("/phones/{phone_id}")
def read_phone(
    phone_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    phone = get_phone_by_id(db, phone_id, current_user.user_id)

    if phone is None:
        raise HTTPException(status_code=404, detail="Phone not found")

    return phone


@router.post("/phones", status_code=status.HTTP_201_CREATED)
def post_phone(
    phone: PhoneCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_phone = create_phone(db, phone, current_user.user_id)

    if new_phone is None:
        raise HTTPException(
            status_code=404,
            detail="Contact not found for this user"
        )

    return new_phone


@router.put("/phones/{phone_id}")
def put_phone(
    phone_id: int,
    phone: PhoneUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated_phone = update_phone(
        db, phone_id, phone, current_user.user_id
    )

    if updated_phone is None:
        raise HTTPException(status_code=404, detail="Phone not found")

    return updated_phone


@router.delete("/phones/{phone_id}")
def remove_phone(
    phone_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deleted_phone = delete_phone(
        db, phone_id, current_user.user_id
    )

    if deleted_phone is None:
        raise HTTPException(status_code=404, detail="Phone not found")

    return {"message": "Phone deleted successfully"}
