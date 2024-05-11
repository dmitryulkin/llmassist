from sqlmodel import Field, SQLModel

__all__ = ["TgBotUser"]


class TgBotUser(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    tgid: int
