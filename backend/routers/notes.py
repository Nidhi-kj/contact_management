
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from main.database import get_db
from models.user import User
from schema.notes import NotesCreate, NotesUpdate
from utils.auth import get_current_user

from CRUD.notes import (
    get_notes,
    get_notes_by_id,
    create_notes,
    update_notes,
    delete_notes
)

router = APIRouter()


# GET ALL NOTES
@router.get("/notes")
def read_notes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_notes(db, current_user.user_id)


# GET NOTE BY ID
@router.get("/notes/{notes_id}")
def read_notes_by_id(
    notes_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    notes = get_notes_by_id(
        db, notes_id, current_user.user_id
    )

    if notes is None:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    return notes


# CREATE NOTE
@router.post("/notes", status_code=status.HTTP_201_CREATED)
def post_notes(
    notes: NotesCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_notes = create_notes(
        db, notes, current_user.user_id
    )

    if new_notes is None:
        raise HTTPException(
            status_code=404,
            detail="Contact not found for this user"
        )

    return new_notes


# UPDATE NOTE
@router.put("/notes/{notes_id}")
def put_notes(
    notes_id: int,
    notes: NotesUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated_notes = update_notes(
        db, notes_id, notes, current_user.user_id
    )

    if updated_notes is None:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    return updated_notes


# DELETE NOTE
@router.delete("/notes/{notes_id}")
def delete_notes_by_id(
    notes_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deleted_notes = delete_notes(
        db, notes_id, current_user.user_id
    )

    if deleted_notes is None:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    return {"message": "Note deleted successfully"}
