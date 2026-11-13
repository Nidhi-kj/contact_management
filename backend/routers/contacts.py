
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from main.database import get_db
from schema.contacts import ContactCreate, ContactUpdate

from CRUD.contacts import (
    get_contacts,
    get_contacts_by_id,
    create_contact,
    update_contact,
    delete_contact
)

from utils.auth import get_current_user
from models.user import User

router = APIRouter()


# Get all contacts of logged-in user
@router.get("/contacts")
def read_contact(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_contacts(db, current_user.user_id)


# Get contact by ID
@router.get("/contacts/{contact_id}")
def read_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    contact = get_contacts_by_id(
        db, contact_id, current_user.user_id
    )

    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")

    return contact


# Create contact

@router.post("/contacts", status_code=201)
def post_contacts(
    contact: ContactCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_contact = create_contact(
        db, contact, current_user.user_id
    )

    if new_contact is None:
        raise HTTPException(
            status_code=404,
            detail="Company not found for this user"
        )

    return new_contact


# Update contact
@router.put("/contacts/{contact_id}")
def put_contacts(
    contact_id: int,
    contact: ContactUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated_contact = update_contact(
        db, contact, contact_id, current_user.user_id
    )

    if updated_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")

    return updated_contact


# Delete contact
@router.delete("/contacts/{contact_id}")
def delete_contacts(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deleted_contact = delete_contact(
        db, contact_id, current_user.user_id
    )

    if deleted_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")

    return {"message": "Contact deleted successfully"}
