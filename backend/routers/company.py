
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from main.database import get_db
from models.user import User
from schema.company import CompanyCreate, CompanyUpdate

from utils.auth import get_current_user

from CRUD.company import (
    get_companies,
    get_company_by_id,
    create_company,
    update_company,
    delete_company
)

router = APIRouter()


# Get logged-in user's companies
@router.get("/companies")
def read_company(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_companies(db, current_user.user_id)


# Get company by ID
@router.get("/companies/{company_id}")
def read_company_by_id(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    company = get_company_by_id(
        db, company_id, current_user.user_id
    )

    if company is None:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    return company


# Create company and link to selected contact
@router.post("/companies", status_code=status.HTTP_201_CREATED)
def post_company(
    company: CompanyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_company = create_company(
        db, company, current_user.user_id
    )

    if new_company is None:
        raise HTTPException(
            status_code=404,
            detail="Contact not found for this user"
        )

    return new_company


# Update company
@router.put("/companies/{company_id}")
def put_company(
    company_id: int,
    company_data: CompanyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    company = update_company(
        db, company_id, company_data, current_user.user_id
    )

    if company is None:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    return company


# Delete company
@router.delete("/companies/{company_id}")
def remove_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    company = delete_company(
        db, company_id, current_user.user_id
    )

    if company is None:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    return {"message": "Company deleted successfully"}
