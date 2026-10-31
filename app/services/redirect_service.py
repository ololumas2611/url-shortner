import logging

from app.models.clicks import Clicks
from app.repositories.click_repo import ClicksRepository
from app.services.url_service import UrlsService


logger = logging.getLogger(__name__)


class RedirectService:
    """
    Responsável por tudo o que acontece quando alguém abre um link curto:
    resolver o código para a URL original e registar o clique.
    """

    def __init__(self, urls_service: UrlsService, clicks_repo: ClicksRepository):
        self.urls = urls_service
        self.clicks = clicks_repo

    def resolve(self, short_code: str, ip: str | None = None,
                user_agent: str | None = None, referer: str | None = None) -> str:

        # Lança ShortCodeNotFoundError (404) se o código não existir.
        code = self.urls.get_short_code(short_code)
        url = self.urls.get_url_of(code)

        self.register_click(code.id, ip, user_agent, referer)

        return url.original_url

    def register_click(self, short_code_id, ip, user_agent, referer) -> None:
        # Se gravar o clique falhar, o utilizador é redirecionado na mesma:
        # perder uma métrica é melhor do que partir o link.
        try:
            self.clicks.save(Clicks(
                short_code_id=short_code_id,
                ip=ip,
                user_agent=user_agent,
                referer=referer,
            ))
        except Exception:
            logger.exception("Não foi possível registar o clique do short code %s", short_code_id)
