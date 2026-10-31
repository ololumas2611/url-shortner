from typing import Callable
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from app.models.urls import Urls
from app.models.short_codes import ShortCodes
from app.core.exceptions import ShortCodeGenerationError


class UrlsRepository:

    def __init__(self, session: Session):
        self.repo = session

    def save(self, original_url: str, gen_code: Callable[[], str], max_attempts: int = 5) -> ShortCodes:
        """
        Grava a URL e o seu código curto na MESMA transação.

        - A URL é inserida primeiro (flush), fora de qualquer savepoint.
        - Cada tentativa de inserir o código corre dentro de um SAVEPOINT:
          se colidir (IntegrityError), volta-se só até ao savepoint e a URL mantém-se.
        - Se todas as tentativas falharem, faz-se rollback de tudo (nem a URL fica).
        - Um único commit no fim: ou fica tudo gravado, ou nada.
        """
        try:
            url = Urls(original_url=original_url)
            self.repo.add(url)
            self.repo.flush()                       # INSERT INTO urls ... (ainda sem commit)

            short_code = None
            for _ in range(max_attempts):
                code = gen_code()
                try:
                    with self.repo.begin_nested():  # SAVEPOINT
                        short_code = ShortCodes(url_id=url.id, code=code)
                        self.repo.add(short_code)
                    break                           # RELEASE SAVEPOINT
                except IntegrityError:
                    short_code = None
                    continue                        # ROLLBACK TO SAVEPOINT -> a url mantém-se
            else:
                raise ShortCodeGenerationError()

            self.repo.commit()                      # URL + código gravados juntos
            self.repo.refresh(short_code)
            return short_code

        except Exception:
            self.repo.rollback()                    # qualquer falha: nada fica gravado
            raise

    def get_by_id(self, url_id: UUID) -> Urls | None:
        # Procura pela chave primária; devolve None se não existir.
        return self.repo.get(Urls, url_id)
