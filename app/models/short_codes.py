
from sqlmodel import SQLModel, Field, TEXT
from uuid import UUID, uuid4
from datetime import datetime, timezone


class ShortCodes(SQLModel, table = True):

    __tablename__ = 'short_codes'

    id : UUID = Field(primary_key=True, default_factory=uuid4)
    url_id : UUID = Field(foreign_key='urls.id', nullable=False)
    code : str = Field(nullable=False, unique=True, max_length=10)
    created_at : datetime = Field(default_factory=lambda : datetime.now(timezone.utc))
    
