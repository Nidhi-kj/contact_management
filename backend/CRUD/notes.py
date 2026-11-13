
from sqlalchemy.orm import Session

from models.notes import Notes
from models.contacts import Contact
from schema.notes import NotesCreate, NotesUpdate


# Current user ke contacts ke notes
def get_notes(db: Session, user_id: int):
    return (
        db.query(Notes)
        .join(Contact, Notes.contact_id == Contact.contact_id)
        .filter(Contact.user_id == user_id)
        .all()
    )


# Note ID se note find karna
def get_notes_by_id(db: Session, notes_id: int, user_id: int):
    return (
        db.query(Notes)
        .join(Contact, Notes.contact_id == Contact.contact_id)
        .filter(
            Notes.notes_id == notes_id,
            Contact.user_id == user_id
        )
        .first()
    )


# Apne contact ke liye note create karna
def create_notes(db: Session, notes: NotesCreate, user_id: int):

    contact = db.query(Contact).filter(
        Contact.contact_id == notes.contact_id,
        Contact.user_id == user_id
    ).first()

    if contact is None:
        return None

    new_notes = Notes(
        contact_id=notes.contact_id,
        notes=notes.notes
    )

    db.add(new_notes)
    db.commit()
    db.refresh(new_notes)

    return new_notes


# Note update
def update_notes(
    db: Session,
    notes_id: int,
    notes_data: NotesUpdate,
    user_id: int
):
    note = get_notes_by_id(db, notes_id, user_id)

    if note is None:
        return None

    update_data = notes_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(note, key, value)

    db.commit()
    db.refresh(note)

    return note


# Note delete
def delete_notes(db: Session, notes_id: int, user_id: int):

    note = get_notes_by_id(db, notes_id, user_id)

    if note is None:
        return None

    db.delete(note)
    db.commit()

    return note
