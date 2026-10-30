from pydantic import BaseModel


class CreateUrl(BaseModel):

    original_url : str 
    