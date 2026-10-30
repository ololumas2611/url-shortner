from fastapi import Depends
from sqlmodel import SQLModel, Session, create_engine
from typing import Annotated
from dotenv import load_dotenv
import os


load_dotenv()


database_url = os.environ.get('DATABASE_URL')

engine = create_engine(database_url)


def create_tables():
    SQLModel.metadata.create_all(engine)

def get_session():

    with Session(engine) as session:
        yield session


session_dp = Annotated[Session, Depends(get_session)]

