from app.repositories.click_repo import ClicksRepository
from app.services.url_service import UrlsService


class ClicksService:

    def __init__(self, urls_service: UrlsService, clicks_repo: ClicksRepository):
        self.urls = urls_service
        self.clicks = clicks_repo

    def count(self, short_code: str) -> int:
        # Lança ShortCodeNotFoundError (404) se o código não existir.
        code = self.urls.get_short_code(short_code)
        return self.clicks.count_by_short_code_id(code.id)
