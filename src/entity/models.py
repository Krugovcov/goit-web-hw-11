from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from datetime import date 
from typing import Optional
class Base(DeclarativeBase):
    pass

class ContactBook(Base):
    __tablename__ = 'contacts'
    id: Mapped[int] = mapped_column(primary_key = True)
    name:Mapped[str] = mapped_column(String(50))
    secondname: Mapped[str] = mapped_column(String(50))
    phone: Mapped[str] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(String(50), nullable=True)
    born_day: Mapped[date] = mapped_column(default=None, nullable=True)
    additional_data: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
