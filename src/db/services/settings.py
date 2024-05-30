from dataclasses import dataclass

from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.services.user import get_user


async def set_user_llm_settings(
    id: int,
    session: AsyncSession,
    *,
    llm_service: str | None = None,
    llm_provider: str | None = None,
    llm_model: str | None = None,
) -> None:
    user = await get_user(id, session)

    if llm_service is not None:
        user.llm_service = llm_service
    if llm_provider is not None:
        user.llm_provider = llm_provider
    if llm_model is not None:
        user.llm_model = llm_model

    session.add(user)
    await session.commit()


@dataclass
class LLMSettings:
    service: str | None
    provider: str | None
    model: str | None


async def get_user_llm_settings(id: int, session: AsyncSession) -> LLMSettings:
    user = await get_user(id, session)

    return LLMSettings(
        service=user.llm_service,
        provider=user.llm_provider,
        model=user.llm_model,
    )
