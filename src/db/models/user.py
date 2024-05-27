from sqlmodel import Field, SQLModel

__all__ = ["User"]


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    admin: bool = False
    llm_service: str | None = None
    llm_provider: str | None = None
    llm_model: str | None = None
