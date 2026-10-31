from app.models.urls import Urls
from app.schemas.url import CreateUrl
from app.repositories.url_repo import UrlsRepository
from app.repositories.short_code_repo import ShortCodesRepository

from string import ascii_letters, digits

import secrets
from urllib.parse import urlsplit

from app.core.exceptions import InvalidUrlError

class UrlsService:

    def __init__(self, urls_repo : UrlsRepository, short_codes_repo : ShortCodesRepository):
        self.urls = urls_repo
        self.short_codes = short_codes_repo

    def gen_random_index(self, chars_length):
        # secrets usa o gerador criptográfico do sistema operativo (imprevisível),
        # ao contrário do random. randbelow(n) devolve 0..n-1, daí o +1.
        return secrets.randbelow(chars_length + 1)

    def gen_short_code(self) -> str:

        BASE = ascii_letters + digits
        base_length = len(BASE) - 1
        code_length = 7
        code = ''

        while len(code) != code_length:

            try:
                random_char = BASE[self.gen_random_index(base_length)]
                if random_char not in code:
                    code += random_char

                if len(code) == code_length:
                    return code

            except Exception as e:
                print("Houve um erro ao gerar ", str(e))
                break
                # ver uma forma melhor de tratar isso.


    def is_valid_url(self, url : str) -> bool:
        # Regra: só URLs absolutas http/https com domínio e sem espaços.
        if not url or any(char.isspace() for char in url):
            return False

        parts = urlsplit(url)
        return parts.scheme in ('http', 'https') and bool(parts.hostname)


    def create(self, create_url : CreateUrl):

        # Só uma URL válida pode gerar um short code.
        if not self.is_valid_url(create_url.original_url):
            raise InvalidUrlError()
        

        short_code = self.urls.save(create_url.original_url, self.gen_short_code)
        return short_code.code