
from sqlalchemy.orm import Session

from models.phone import Phone
from models.contacts import Contact
from schema.phone import PhoneCreate, PhoneUpdate


# Sirf current user ke contacts ke phone numbers
def get_phones(db: Session, user_id: int):
    return (
        db.query(Phone)
        .join(Contact, Phone.contact_id == Contact.contact_id)
        .filter(Contact.user_id == user_id)
        .all()
    )


# Phone ID se phone find karna, ownership check ke saath
def get_phone_by_id(db: Session, phone_id: int, user_id: int):
    return (
        db.query(Phone)
        .join(Contact, Phone.contact_id == Contact.contact_id)
        .filter(
            Phone.phone_id == phone_id,
            Contact.user_id == user_id
        )
        .first()
    )


# Sirf apne contact ke liye phone create karna
def create_phone(db: Session, phone: PhoneCreate, user_id: int):

    contact = db.query(Contact).filter(
        Contact.contact_id == phone.contact_id,
        Contact.user_id == user_id
    ).first()

    if contact is None:
        return None

    new_phone = Phone(
        contact_id=phone.contact_id,
        phone=phone.phone
    )

    db.add(new_phone)
    db.commit()
    db.refresh(new_phone)

    return new_phone


# Phone update
def update_phone(
    db: Session,
    phone_id: int,
    phone_data: PhoneUpdate,
    user_id: int
):
    phone = get_phone_by_id(db, phone_id, user_id)

    if phone is None:
        return None

    update_data = phone_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(phone, key, value)

    db.commit()
    db.refresh(phone)

    return phone


# Phone delete
def delete_phone(db: Session, phone_id: int, user_id: int):

    phone = get_phone_by_id(db, phone_id, user_id)

    if phone is None:
        return None

    db.delete(phone)
    db.commit()

    return phone
