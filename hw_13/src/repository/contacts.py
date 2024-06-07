from datetime import date, timedelta
from typing import List, Optional
from sqlalchemy import or_, and_, func
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession


from src import schemas
from src.database.models import Contact, User
from src.schemas.contact import ContactBase


async def get_contacts(skip: int, limit: int, db: AsyncSession, user: User) -> List[Contact]:
    query = select(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


async def get_contact(contact_id: int, db: AsyncSession, user: User) -> Optional[Contact]:
    query = select(Contact).filter(Contact.id == contact_id, Contact.user_id == user.id)
    result = await db.execute(query)
    return result.scalars().first()


async def create_contact(contact: schemas.contact.ContactCreate, db: AsyncSession, user: User):
    db_contact = Contact(**contact.dict(), user_id=user.id)
    db.add(db_contact)
    await db.commit()
    await db.refresh(db_contact)
    return db_contact


async def update_contact(contact_id: int, body: ContactBase, db: AsyncSession, user: User) -> Optional[Contact]:
    query = select(Contact).filter(Contact.id == contact_id, Contact.user_id == user.id)
    result = await db.execute(query)
    contact = result.scalars().first()
    if contact:
        for key, value in body.dict().items():
            setattr(contact, key, value)
        await db.commit()
        await db.refresh(contact)
    return contact


async def remove_contact(contact_id: int, db: AsyncSession, user: User) -> Optional[Contact]:
    query = select(Contact).filter(Contact.id == contact_id, Contact.user_id == user.id)
    result = await db.execute(query)
    contact = result.scalars().first()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact


async def search_contacts(db: AsyncSession, query: str, user: User) -> List[Contact]:
    query = select(Contact).filter(
        or_(
            Contact.first_name.contains(query),
            Contact.last_name.contains(query),
            Contact.email.contains(query)
        ), Contact.user_id == user.id
    )
    result = await db.execute(query)
    return result.scalars().all()


async def get_upcoming_birthdays(db: AsyncSession, user: User) -> List[Contact]:
    today = date.today()
    upcoming = today + timedelta(days=7)

    today_str = today.strftime('%m-%d')
    upcoming_str = upcoming.strftime('%m-%d')

    query = select(Contact).filter(
        Contact.user_id == user.id,
        or_(
            and_(
                func.to_char(Contact.birthday, 'MM-DD') >= today_str,
                func.to_char(Contact.birthday, 'MM-DD') <= upcoming_str
            )
        )
    )

    result = await db.execute(query)
    contacts = result.scalars().all()
    return contacts
