from typing import List
from libgravatar import Gravatar
from sqlalchemy.orm import Session

from src.database.models import User, Contact
from src.schemas import ContactBase, ContactStatusUpdate, UserModel
from datetime import datetime  as dtdt

async def get_user_by_email(email: str, db: Session) -> User:
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.dict(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    user.refresh_token = token
    db.commit()

async def confirmed_email(email: str, db: Session) -> None:
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()

async def get_contacts(skip: int, limit: int, user: User, db: Session,) -> List[Contact]:
    return db.query(Contact).filter(Contact.user_id==user.id).offset(skip).limit(limit).all()

async def get_contacts_birthdays(skip: int, limit: int, user: User, db: Session,) -> List[Contact]:
    users = db.query(Contact).filter(Contact.user_id==user.id).offset(skip).limit(limit).all()
    now = dtdt.today().date()
    birthdays = []
    for user in users:
        date_user = user.date_of_birth
        week_day = date_user.isoweekday()
        difference_day = (date_user.day - now.day)
        if 0 <= difference_day < 7 :
            if difference_day < 6 :
                birthdays.append(user)
            else:
                if difference_day == 7:
                    birthdays.append(user)
                elif difference_day == 6:
                    birthdays.append(user)
    return birthdays
        
async def get_contact(user_id: int, user:User, db: Session) -> User:
    return db.query(Contact).filter(Contact.user_id==user.id).filter(Contact.id == user_id).first()

async def get_contact_name(name: str, surname:str, email_address:str, phone_number: str, user:User, db: Session) -> Contact:
    if db.query(Contact).filter(Contact.user_id==user.id).first():
        if name:
            return db.query(Contact).filter(Contact.name == name).first()
        elif surname:
            return db.query(Contact).filter(Contact.surname == surname).first()
        elif email_address:
            return db.query(Contact).filter(Contact.email_address == email_address).first()
        elif phone_number:
            return db.query(Contact).filter(Contact.phone_number== phone_number).first()

async def create_contact(body: ContactBase, user:User, db: Session) -> Contact:
    user = Contact(name=body.name, surname=body.surname, email_address=body.email_address,
                    phone_number=body.phone_number, date_of_birth = body.date_of_birth,
                      additional_data = body.additional_data, user_id=user.id)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

async def remove_user(user_id: int, user:User, db: Session) -> Contact | None:
    user = db.query(Contact).filter(Contact.user_id==user.id).filter(Contact.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user


async def update_contact(user_id: int, body: ContactBase, user:User, db: Session) -> Contact | None:
    user = db.query(Contact).filter(Contact.user_id==user.id).filter(Contact.id == user_id).first()
    if user:
        user.name = body.name
        user.surname = body.surname
        user.email_address = body.email_address
        user.phone_number = body.phone_number
        user.date_of_birth = body.date_of_birth
        user.additional_data = body.additional_data
        db.commit()
    return user


async def update_status_user(user_id: int, body: ContactStatusUpdate, user:User, db: Session) -> Contact | None:
    user = db.query(Contact).filter(Contact.user_id==user.id).filter(Contact.id == user_id).first()
    if user:
        user.done = body.done
        db.commit()
    return user
