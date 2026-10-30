from fastapi import APIRouter, Depends
from app.schemas.url import CreateUrl
from app.db.database import session_dp
from app.services.url_service import UrlsService
from app.api.routes.dependecy import get_url_service



urls_route = APIRouter(prefix='/urls', tags=['urls, url'])


@urls_route.get("/")
def get():
    pass

@urls_route.post("/")
def create(create_url : CreateUrl, url_service : UrlsService = Depends(get_url_service)):
    short_code = url_service.create(create_url)
    return {
        'original_url': create_url.original_url,
        'short_code': short_code,
    }