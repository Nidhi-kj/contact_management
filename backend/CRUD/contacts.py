# Database mein create, read, update, delete karta hai

from sqlalchemy.orm import Session
# from main.models.contacts import Contact
from models.contacts import Contact
from models.company import Company
 
# def get_contacts(db:Session):
#     return db.query(Contact).all()
def get_contacts(db: Session, user_id: int):
    return db.query(Contact).filter(
        Contact.user_id == user_id
    ).all()


def get_contacts_by_id(db:Session,contact_id : int , user_id: int):
    return db.query(Contact).filter(
        Contact.contact_id == contact_id,
        Contact.user_id == user_id
    ).first()

def create_contact(db: Session, contact_data, user_id: int):

    if contact_data.company_id is not None:
        company = db.query(Company).join(
            Contact,
            Contact.company_id == Company.company_id
        ).filter(
            Company.company_id == contact_data.company_id,
            Contact.user_id == user_id
        ).first()

        if company is None:
            return None

    new_contact = Contact(
        user_id=user_id,
        company_id=contact_data.company_id,
        name=contact_data.name,
        email=contact_data.email,
        phone=contact_data.phone
    )

    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)

    return new_contact

def update_contact(db: Session, contact_data, contact_id: int, user_id: int):

    contact = db.query(Contact).filter(
        Contact.contact_id == contact_id,
        Contact.user_id == user_id
    ).first()

    if contact is None:
        return None

    update_data = contact_data.model_dump(exclude_unset=True)

    if "company_id" in update_data and update_data["company_id"] is not None:

        company = db.query(Company).join(
            Contact,
            Contact.company_id == Company.company_id
        ).filter(
            Company.company_id == update_data["company_id"],
            Contact.user_id == user_id
        ).first()

        if company is None:
            return None

    for key, value in update_data.items():
        setattr(contact, key, value)

    db.commit()
    db.refresh(contact)

    return contact


def delete_contact(db:Session , contact_id: int,user_id: int):
    contact = db.query(Contact).filter(
        Contact.contact_id == contact_id,
        Contact.user_id == user_id
    ).first()
    if contact is None:
        return None

    db.delete(contact)
    db.commit()

    return contact


    
    

