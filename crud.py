from typing import Optional

from sqlalchemy import extract, cast, Date
from sqlalchemy.orm import Session
from models import Contact
import schemas
from datetime import date, timedelta


def create_contact(db: Session, contact: schemas.ContactCreate):
    db_contact = Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def get_contact(db: Session, contact_id: int):
    return db.query(Contact).filter(Contact.id == contact_id).first()


def get_contacts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Contact).offset(skip).limit(limit).all()


def upgrade_contact(db: Session, contact_id: int, contact: schemas.ContactCreate):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact:
        for key, value in contact.dict.items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact


def delete_contact(db: Session, contact_id: int):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact:
        db.delete(db_contact)
        db.commit()
        return db_contact
    else:
        return None


def search_contacts(db: Session, first_name: Optional[str] = None, second_name: Optional[str] = None, email: Optional[str] = None):
    query = db.query(Contact)
    if first_name:
        query = query.filter((Contact.first_name.ilike(f"%{first_name}%")))
    if second_name:
        query = query.filter((Contact.first_name.ilike(f"%{second_name}%")))
    if email:
        query = query.filter(Contact.email.ilike(f"%{email}%"))
    return query.all()


def get_upcoming_birthdays(session: Session):
    today = date.today()
    seven_days_later = today + timedelta(days=7)
    contacts_with_upcoming_birthdays = session.query(Contact).filter(
        extract('month', cast(Contact.birthdate, Date)) == today.month,
        extract('day', cast(Contact.birthdate, Date)) >= today.day,
        extract('day', cast(Contact.birthdate, Date)) <= seven_days_later.day
    ).all()
    if today.month != seven_days_later.month:
        contacts_with_upcoming_birthdays += session.query(Contact).filter(
            extract('month', cast(Contact.birthdate, Date)) == seven_days_later.month,
            extract('day', cast(Contact.birthdate, Date)) <= seven_days_later.day
        ).all()
    return contacts_with_upcoming_birthdays
