from sqlmodel import SQLModel, Field, TEXT
from uuid import UUID, uuid4
from datetime import datetime, timezone


class Urls(SQLModel, table = True):

    __tablename__ = 'urls'

    id : UUID = Field(primary_key=True, default_factory=uuid4())
    original_url : str = Field(sa_type=TEXT, nullable=False)
    created_at : datetime = Field(default_factory=lambda : datetime.now(timezone.utc))
    