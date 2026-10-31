from uuid import UUID

from sqlmodel import Session, select, func

from app.models.clicks import Clicks


class ClicksRepository:

    def __init__(self, session: Session):
        self.repo = session

    def save(self, click: Clicks) -> Clicks:
        try:
            self.repo.add(click)
            self.repo.commit()
            return click
        except Exception:
            self.repo.rollback()
            raise

    def count_by_short_code_id(self, short_code_id: UUID) -> int:
        # SELECT count(*) FROM clicks WHERE short_code_id = ...
        statement = select(func.count()).select_from(Clicks).where(Clicks.short_code_id == short_code_id)
        return self.repo.exec(statement).one()
