from sqlmodel import SQLModel, Field, TEXT
from uuid import UUID, uuid4
from datetime import datetime, timezone


class Clicks(SQLModel, table = True):

    __tablename__ = 'clicks'

    id : UUID = Field(primary_key=True, default_factory=uuid4)
    # index: as métricas vão filtrar quase sempre por short code
    short_code_id : UUID = Field(foreign_key='short_codes.id', nullable=False, index=True)
    clicked_at : datetime = Field(default_factory=lambda : datetime.now(timezone.utc))

    # Dados do pedido — opcionais, porque nem todos os clientes os enviam
    ip : str | None = Field(default=None, max_length=45)          # 45 = tamanho máximo de um IPv6
    user_agent : str | None = Field(default=None, sa_type=TEXT)
    referer : str | None = Field(default=None, sa_type=TEXT)
