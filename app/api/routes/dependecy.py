from app.db.database import session_dp
from app.services.url_service import UrlsService
from app.repositories.url_repo import UrlsRepository



def get_url_service(session : session_dp):
    url_repo = UrlsRepository(session)
    return UrlsService(url_repo)

