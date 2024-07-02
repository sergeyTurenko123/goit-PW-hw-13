from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.database.models import User
from src.schemas import ContactBase, ContactStatusUpdate, ContactResponse
from src.repository import users as repository_users
from src.services.auth import auth_service

router = APIRouter(prefix='/users')

@router.get("/",  response_model=List[ContactResponse])
async def read_users(birthdays: bool, skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                     current_user: User = Depends(auth_service.get_current_user)):
    users_birthdays = await repository_users.get_contacts_birthdays(skip, limit, current_user, db)
    users_all = await repository_users.get_contacts(skip, limit, current_user, db)
    if birthdays:
        return users_birthdays
    else:
        return users_all

@router.get("/{contact_id}", response_model=ContactResponse)
async def read_user(contact_id: int, db: Session = Depends(get_db),
                    current_user: User = Depends(auth_service.get_current_user)):
    user = await repository_users.get_contact(contact_id, current_user, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.get("/contact/", response_model=ContactResponse)
async def read_user(name: str| None=None, surname:  str| None=None, email_address: str| None=None,
                     phone_number: str| None=None, db: Session = Depends(get_db),
                     current_user: User = Depends(auth_service.get_current_user)):
    user = await repository_users.get_contact_name(name, surname, email_address, phone_number,
                                                current_user, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_user(body: ContactBase, db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    return await repository_users.create_contact(body, current_user, db)


@router.put("/{user_id}", response_model=ContactResponse)
async def update_user(body: ContactBase, user_id: int, db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    user = await repository_users.update_contact(user_id, body, current_user, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.patch("/{user_id}", response_model=ContactResponse)
async def update_status_user(body: ContactStatusUpdate, user_id: int, db: Session = Depends(get_db),
                             current_user: User = Depends(auth_service.get_current_user)):
    user = await repository_users.update_status_user(user_id, body, current_user, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.delete("/{user_id}", response_model=ContactResponse)
async def remove_user(user_id: int, db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    user = await repository_users.remove_user(user_id, current_user, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user