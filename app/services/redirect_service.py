from app.services.url_service import UrlsService


class RedirectService:
    """
    Responsável por tudo o que acontece quando alguém abre um link curto.

    Hoje só resolve o código para a URL original; é aqui que vai entrar
    o registo dos cliques, sem mexer no UrlsService nem na rota.
    """

    def __init__(self, urls_service: UrlsService):
        self.urls = urls_service

    def resolve(self, short_code: str) -> str:
        # Lança ShortCodeNotFoundError (404) se o código não existir.
        url = self.urls.get_by_short_code(short_code)
        return url.original_url
