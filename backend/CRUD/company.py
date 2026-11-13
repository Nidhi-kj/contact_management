
from sqlalchemy.orm import Session

from models.company import Company
from models.contacts import Contact
from schema.company import CompanyCreate, CompanyUpdate


# Get companies belonging to logged-in user's contacts
def get_companies(db: Session, user_id: int):

    return (
        db.query(Company)
        .join(Contact, Contact.company_id == Company.company_id)
        .filter(Contact.user_id == user_id)
        .distinct()
        .all()
    )


# Get one company only if linked to user's contact
def get_company_by_id(db: Session, company_id: int, user_id: int):

    return (
        db.query(Company)
        .join(Contact, Contact.company_id == Company.company_id)
        .filter(
            Company.company_id == company_id,
            Contact.user_id == user_id
        )
        .first()
    )


# Create company and link it to selected contact
def create_company(db: Session, company: CompanyCreate, user_id: int):

    contact = db.query(Contact).filter(
        Contact.contact_id == company.contact_id,
        Contact.user_id == user_id
    ).first()

    if contact is None:
        return None

    new_company = Company(
        name=company.name,
        website=company.website,
        phone=company.phone
    )

    db.add(new_company)
    db.flush()

    contact.company_id = new_company.company_id

    db.commit()
    db.refresh(new_company)

    return new_company


# Update company
def update_company(
    db: Session,
    company_id: int,
    company_data: CompanyUpdate,
    user_id: int
):

    company = get_company_by_id(db, company_id, user_id)

    if company is None:
        return None

    update_data = company_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(company, key, value)

    db.commit()
    db.refresh(company)

    return company


# Delete company
def delete_company(db: Session, company_id: int, user_id: int):

    company = get_company_by_id(db, company_id, user_id)

    if company is None:
        return None

    # Unlink company from its contacts before deleting
    db.query(Contact).filter(
        Contact.company_id == company_id,
        Contact.user_id == user_id
    ).update(
        {Contact.company_id: None},
        synchronize_session=False
    )

    db.delete(company)
    db.commit()

    return company
