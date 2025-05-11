from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.note_schemas import NoteCreate, NoteUpdate, NoteOut
from app.schemas.response_schemas import SuccessResponse, success_response, error_response
from typing import List
from app.db.models import Note

router = APIRouter(prefix="/notes", tags=["Notes"])

@router.get("/", response_model=SuccessResponse)
def list_notes(db: Session = Depends(get_db)):
    notes = db.query(Note).all()
    return success_response("Fetched notes successfully.", notes)

@router.post("/", response_model=SuccessResponse)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    new_note = Note(**note.model_dump())
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return success_response("Note created successfully.", new_note)

@router.get("/{note_id}", response_model=SuccessResponse)
def get_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        return error_response("Note not found.")
    return success_response("Note fetched successfully.", note)

@router.put("/{note_id}", response_model=SuccessResponse)
def update_note(note_id: int, note: NoteUpdate, db: Session = Depends(get_db)):
    note_to_update = db.query(Note).filter(Note.id == note_id).first()
    if not note_to_update:
        return error_response("Note not found.")
    note_to_update.update(**note.model_dump())
    db.commit()
    db.refresh(note_to_update)
    return success_response("Note updated successfully.", note_to_update)

@router.delete("/{note_id}", response_model=SuccessResponse)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note_to_delete = db.query(Note).filter(Note.id == note_id).first()
    if not note_to_delete:
        return error_response("Note not found.")
    db.delete(note_to_delete)
    db.commit()
    return success_response("Note deleted successfully.")

