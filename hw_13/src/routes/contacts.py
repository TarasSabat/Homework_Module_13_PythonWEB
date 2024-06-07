from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.ext.asyncio import AsyncSession
from src import schemas
from src.database.db import get_db
from src.database.models import User
from src.schemas.contact import ContactUpdate
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service


router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.post("/", response_model=schemas.contact.Contact, status_code=status.HTTP_201_CREATED, dependencies=[Depends(
    RateLimiter(seconds=30))])
async def create_contact(body: schemas.contact.ContactCreate, db: AsyncSession = Depends(get_db), user: User
= Depends(auth_service.get_current_user)):
    return await repository_contacts.create_contact(body, db, user)


@router.get("/", response_model=List[schemas.contact.Contact], status_code=status.HTTP_201_CREATED, dependencies=[Depends(
    RateLimiter(times=1, seconds=20))])
async def read_contacts(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db), user: User
= Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_contacts(skip, limit, db, user)
    return contacts


@router.get("/{contact_id}", response_model=schemas.contact.Contact, status_code=status.HTTP_201_CREATED, dependencies=[Depends(
    RateLimiter(times=1, seconds=20))])
async def read_contact(contact_id: int, db: AsyncSession = Depends(get_db), user: User
= Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact(contact_id, db, user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.put("/{contact_id}", response_model=schemas.contact.Contact)
async def update_contact(contact_id: int, body: ContactUpdate, db: AsyncSession = Depends(get_db), user: User
= Depends(auth_service.get_current_user)):
    contact = await repository_contacts.update_contact(contact_id, body, db, user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", response_model=schemas.contact.Contact)
async def remove_contact(contact_id: int, db: AsyncSession = Depends(get_db), user: User
= Depends(auth_service.get_current_user)):
    contact = await repository_contacts.remove_contact(contact_id, db, user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.get("/search/", response_model=List[schemas.contact.Contact], status_code=status.HTTP_201_CREATED, dependencies=[Depends(
    RateLimiter(times=1, seconds=20))])
async def search_contacts(query: str, db: AsyncSession = Depends(get_db), user: User
= Depends(auth_service.get_current_user)):
    contact = await repository_contacts.search_contacts(db, query, user)
    return contact


@router.get("/upcoming_birthdays/", response_model=List[schemas.contact.Contact])
async def upcoming_birthdays(db: AsyncSession = Depends(get_db), user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_upcoming_birthdays(db, user)
    return contact
