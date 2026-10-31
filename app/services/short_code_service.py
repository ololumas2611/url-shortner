from app.repositories.short_code_repo import ShortCodesRepository


class ShortCodesService:

    def __init__(self, short_codes_repo: ShortCodesRepository):
        self.short_codes = short_codes_repo
