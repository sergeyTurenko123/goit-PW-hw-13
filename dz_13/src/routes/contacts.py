from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.database.models import User
from src.schemas import ContactBase, ContactResponse, ContactStatusUpdate
from src.repository import users as repository_users
from src.services.auth import auth_service
from fastapi_limiter.depends import RateLimiter

router = APIRouter(prefix='/contacts')

@router.get("/",  response_model=List[ContactResponse], dependencies=[Depends(RateLimiter(times=1, seconds=20))])
async def read_contacts(birthdays: bool, skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                     current_user: User = Depends(auth_service.get_current_user)):
    contacts_birthdays = await repository_users.get_contacts_birthdays(skip, limit, current_user, db)
    contacts_all = await repository_users.get_contacts(skip, limit, current_user, db)
    if birthdays:
        return contacts_birthdays
    else:
        return contacts_all

@router.get("/{contact_id}", response_model=ContactResponse, dependencies=[Depends(RateLimiter(times=1, seconds=20))])
async def read_contact(contact_id: int, db: Session = Depends(get_db),
                    current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_users.get_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return contact

@router.get("/contact/", response_model=ContactResponse, dependencies=[Depends(RateLimiter(times=1, seconds=20))])
async def read_contact(name: str| None=None, surname:  str| None=None, email_address: str| None=None,
                     phone_number: str| None=None, db: Session = Depends(get_db),
                     current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_users.get_contact_name(name, surname, email_address, phone_number,
                                                current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return contact

@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED, 
             dependencies=[Depends(RateLimiter(times=1, seconds=20))])
async def create_contact(body: ContactBase, db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    return await repository_users.create_contact(body, current_user, db)


@router.put("/{contact_id}", response_model=ContactResponse, dependencies=[Depends(RateLimiter(times=1, seconds=20))])
async def update_contact(body: ContactBase, contact_id: int, db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_users.update_contact(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return contact


@router.patch("/{contact_id}", response_model=ContactResponse)
async def update_status_contact(body: ContactStatusUpdate, contact_id: int, db: Session = Depends(get_db),
                             current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_users.update_status_user(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(contact_id: int, db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_users.remove_user(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return contact