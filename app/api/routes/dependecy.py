from app.db.database import session_dp
from app.services.url_service import UrlsService
from app.repositories.url_repo import UrlsRepository
from app.repositories.short_code_repo import ShortCodesRepository



def get_url_service(session : session_dp):
    url_repo = UrlsRepository(session)
    short_codes_repo = ShortCodesRepository(session)
    return UrlsService(url_repo, short_codes_repo)

