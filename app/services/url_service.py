from app.models.urls import Urls
from app.schemas.url import CreateUrl
from app.repositories.url_repo import UrlsRepository

from string import ascii_letters, digits

import secrets

class UrlsService:

    def __init__(self, urls_repo : UrlsRepository):
        self.urls = urls_repo

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



    def create(self, create_url : CreateUrl):
        short_code = self.urls.save(create_url.original_url, self.gen_short_code)
        return short_code.code