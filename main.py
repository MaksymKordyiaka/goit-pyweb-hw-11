from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from connect_db import get_db
import crud
import schemas

app = FastAPI()


@app.post('/contacts', response_model=schemas.Contact)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    db_contact = crud.create_contact(db=db, contact=contact)
    return db_contact


@app.get('/contacts/{contact_id}', response_model=schemas.Contact)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = crud.get_contact(db, contact_id)
    if db_contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found')
    return db_contact


@app.get('/contacts', response_model=list[schemas.Contact])
def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_contacts = crud.get_contacts(db, skip=skip, limit=limit)
    if db_contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No contacts found')
    return db_contacts


@app.put('/contacts/{contact_id}', response_model=schemas.Contact)
def update_contact(contact_id: int, contact_update: schemas.ContactCreate, db: Session = Depends(get_db)):
    db_contact = crud.upgrade_contact(db, contact_id, contact_update)
    if db_contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found')
    return db_contact


@app.delete('/contacts/{contact_id}', response_model=schemas.Contact)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = crud.delete_contact(db, contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact
