from sqlmodel import Session, select

from app.models.short_codes import ShortCodes


class ShortCodesRepository:

    def __init__(self, session: Session):
        self.repo = session

    def get_by_code(self, code: str) -> ShortCodes | None:
        statement = select(ShortCodes).where(ShortCodes.code == code)
        return self.repo.exec(statement).first()
