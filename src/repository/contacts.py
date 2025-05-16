from datetime import date, datetime, timedelta
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from src.entity.models import ContactBook
from src.schemas.contact import ContactBookSchema, ContactBookSchemaUpdateSchema



async def get_contacts(limit: int, offset: int, db: AsyncSession, name: str = None, secondname: str = None, email: str = None):
    stmt = select(ContactBook).offset(offset).limit(limit)
    if name:
        stmt = stmt.filter(ContactBook.name.ilike(f'%{name}%'))
    if secondname:
        stmt = stmt.filter(ContactBook.secondname.ilike(f'%{secondname}%'))
    if email:
        stmt = stmt.filter(ContactBook.email.ilike(f'%{email}%'))
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_contacts_birthday(db: AsyncSession):
    today = datetime.today().date()
    seven_days_later = today + timedelta(days=7)
    
    stmt = select(ContactBook).filter(
        or_(
            # Для случая, когда период не пересекает новый год
            (ContactBook.born_day >= today) & (ContactBook.born_day <= seven_days_later),
            # Для случая перехода через новый год (например, декабрь-январь)
            (ContactBook.born_day >= date(today.year, 1, 1)) & 
            (ContactBook.born_day <= date(today.year, 1, 7)) & 
            (today.month == 12)
        )
    )
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_contact_by_id(contact_id: int, db: AsyncSession):
    stmt = select(ContactBook).filter_by(id=contact_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_contact(body: ContactBookSchema, db:AsyncSession):
    contact = ContactBook(**body.model_dump(exclude_unset=True))
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


async def update_contact(contact_id:int, body: ContactBookSchemaUpdateSchema, db:AsyncSession ):
    stmt = select(ContactBook).filter_by(id = contact_id)
    result = await db.execute(stmt)
    contact = result.scalar_one_or_none()
    if contact:
        update_data = body.dict(exclude_unset=True)  # тільки передані поля
        for key, value in update_data.items():
            setattr(contact, key, value)  # оновлює значення контактів
        await db.commit()
        await db.refresh(contact)
    return contact
    



async def delete_contact(contact_id: int, db:AsyncSession):
    stmt = select(ContactBook).filter_by(id=contact_id)
    contact = await db.execute(stmt)
    contact = contact.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact