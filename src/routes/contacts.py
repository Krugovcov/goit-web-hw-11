from fastapi import APIRouter, HTTPException, Depends, status, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.repository import contacts as repositories_contacts
from src.schemas.contact import ContactBookSchema, ContactBookSchemaUpdateSchema, ContactBookResponse
router = APIRouter(prefix='/contacts', tags=['contacts'])


@router.get('/birthday', response_model=list[ContactBookResponse])
async def birthday(db: AsyncSession = Depends(get_db)):
    try:
        contacts = await repositories_contacts.get_contacts_birthday(db)
        if not contacts:
            return []
        return contacts
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get('/', response_model=list[ContactBookResponse])
async def get_contacts(
    limit: int = Query(10, ge=10, le=500), 
    offset: int = Query(0, ge=0),
    name: str = Query(None, alias="name", description="Search contacts by name"), 
    secondname: str = Query(None, alias="secondname", description="Search contacts by secondname"), 
    email: str = Query(None, alias="email", description="Search contacts by email"), 
    db: AsyncSession = Depends(get_db)
):
    contacts = await repositories_contacts.get_contacts(limit, offset, db, name, secondname, email)
    return contacts

@router.get('/{contact_id}', response_model=ContactBookResponse)
async def get_contact_by_id(contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db)):
    contact = await repositories_contacts.get_contact_by_id(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

@router.post('/', response_model=ContactBookResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body:ContactBookSchema, db:AsyncSession = Depends(get_db)):
    contact = await repositories_contacts.create_contact(body, db)
    return contact

@router.put('/{contact_id}')
async def update_contact(body:ContactBookSchemaUpdateSchema,contact_id:int = Path(ge=1), db:AsyncSession=Depends(get_db)):
    contact = await repositories_contacts.update_contact(contact_id, body, db )
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return contact


@router.delete('/{contact_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int = Path(he=1), db:AsyncSession = Depends(get_db)):
    contact = await repositories_contacts.delete_contact(contact_id, db)



