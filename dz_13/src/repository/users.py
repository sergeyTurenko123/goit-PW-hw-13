from typing import List
from libgravatar import Gravatar
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User, Contact
from src.schemas import ContactBase, ContactStatusUpdate, UserModel
from datetime import datetime  as dtdt

async def get_user_by_email(email: str, db: Session) -> User:
    """
    Gets user by email.
    :param email: User email.
    :type email: str
    :param db: The database session.
    :type db: Session
    """
    return db.query(User).filter(User.email == email).first()

async def update_avatar(email: str, url: str | None, db: AsyncSession) -> User:
    """
    Updates the user's avatar.
    :param email: User email.
    :type email: str
    :param url: Image address.
    :type url: str
    :param db: The database session.
    :type db: Session
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user

async def create_user(body: UserModel, db: Session) -> User:
    """
    Creates a user.
    :param body: User data.
    :type body: str
    :param db: The database session.
    :type db: Session
    """
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
    """
    Update token.
    :param user: User data.
    :type user: str
    :param token: refresh token.
    :type token: str
    :param db: The database session.
    :type db: Session
    """
    user.refresh_token = token
    db.commit()

async def confirmed_email(email: str, db: Session) -> None:
    """
    Confirms email address.
    :param email: User email.
    :type user: str
    :param db: The database session.
    :type db: Session
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()

async def get_contacts(skip: int, limit: int, user: User, db: Session,) -> List[Contact]:
    """
    Receives contacts.
    :param skip: How many records to skip from the beginning.
    :type skip: int
    :param limit: The number of records to output.
    :type limit: int
    :param user: User.
    :type user: str
    :param db: The database session.
    :type db: Session
    """
    return db.query(Contact).filter(Contact.user_id==user.id).offset(skip).limit(limit).all()

async def get_contacts_birthdays(skip: int, limit: int, user: User, db: Session,) -> List[Contact]:
    """
    Receives birthday contacts in seven days.
    :param skip: How many records to skip from the beginning.
    :type skip: int
    :param limit: The number of records to output.
    :type limit: int
    :param user: User.
    :type user: str
    :param db: The database session.
    :type db: Session
    """
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
    """
    Search the contact by its id.
    :param user_id: id contact.
    :type user_id: int
    :param user: User.
    :type user: str
    :param db: The database session.
    :type db: Session
    """
    return db.query(Contact).filter(Contact.user_id==user.id).filter(Contact.id == user_id).first()

async def get_contact_name(name: str, surname:str, email_address:str, phone_number: str, user:User, db: Session) -> Contact:
    """
    Search for a contact by his name, last name, email, phone number.
    :param name: name.
    :type name: int
    :param surname: surname.
    :type surname: str
    :param email_address: email address.
    :type email_address: str
    :param phone_number: phone number.
    :type phone_number: str
    :param user: User.
    :type user: str
    :param db: The database session.
    :type db: Session
    """
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
    """
    Creates a contact.
    :param body: contact details.
    :type body: str
    :param user: User.
    :type user: str
    :param db: The database session.
    :type db: Session
    """
    user = Contact(name=body.name, surname=body.surname, email_address=body.email_address,
                    phone_number=body.phone_number, date_of_birth = body.date_of_birth,
                      additional_data = body.additional_data, user_id=user.id)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

async def remove_contact(contact_id: int, user:User, db: Session) -> Contact | None:
    """
    Delete a contact.
    :param contact_id: contact id.
    :type contact_id: int
    :param user: User.
    :type user: str
    :param db: The database session.
    :type db: Session
    """
    contact = db.query(Contact).filter(Contact.user_id==user.id).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def update_contact(contact_id: int, body: ContactBase, user:User, db: Session) -> Contact | None:
    """
    Update a contact.
    :param contact_id: contact id.
    :type contact_id: int
    :param body: contact details.
    :type body: str
    :param user: User.
    :type user: str
    :param db: The database session.
    :type db: Session
    """
    user = db.query(Contact).filter(Contact.user_id==user.id).filter(Contact.id == contact_id).first()
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
    """
    Update status user.
    :param user_id: user id.
    :type user_id: int
    :param body: User status.
    :type body: bool
    :param user: User.
    :type user: str
    :param db: The database session.
    :type db: Session
    """
    user = db.query(Contact).filter(Contact.user_id==user.id).filter(Contact.id == user_id).first()
    if user:
        user.done = body.done
        db.commit()
    return user
