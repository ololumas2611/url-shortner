from fastapi import APIRouter
from app.schemas.url import CreateUrl

urls_route = APIRouter(prefix='/urls', tags=['urls, url'])


@urls_route.get("/")
def get():
    pass

@urls_route.post("/")
def create(create_url : CreateUrl):
    return f'URL original: {create_url.original_url}'