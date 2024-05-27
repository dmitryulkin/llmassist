from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlmodel.ext.asyncio.session import AsyncSession

from src.aiogram_bot.db.tg_user import get_user_id
from src.aiogram_bot.keyboards.inline.settings import (
    LLMModelCallbackFactory,
    LLMProviderCallbackFactory,
    LLMServiceCallbackFactory,
    llm_model_choose_keyboard,
    llm_provider_choose_keyboard,
    llm_service_choose_keyboard,
    llm_settings_keyboard,
    settings_keyboard,
)
from src.db.services.settings import (
    get_user_llm_settings,
    set_user_llm_settings,
)

router = Router(name="settings")


@router.message(Command(commands=["settings"]))
async def settings_handler(message: Message) -> None:
    await message.answer("Settings:", reply_markup=settings_keyboard())


@router.callback_query(F.data == "cancel")
async def settings_cancel_handler(
    call: CallbackQuery, state: FSMContext
) -> None:
    await state.clear()
    if isinstance(call.message, Message):
        await call.message.edit_text("Cancelled.")


@router.callback_query(F.data == "llm_settings")
async def llm_settings_handler(
    call: CallbackQuery, state: FSMContext, session: AsyncSession
) -> None:
    if isinstance(call.message, Message):
        await call.message.edit_text("LLM Settings:")

        app_user_id = await get_user_id(call.from_user.id, session)
        llm_settings = await get_user_llm_settings(app_user_id, session)
        data = await state.update_data(
            service=llm_settings.service,
            provider=llm_settings.provider,
            model=llm_settings.model,
        )

        await call.message.edit_reply_markup(
            reply_markup=llm_settings_keyboard(
                data["service"], data["provider"]
            )
        )


@router.callback_query(F.data == "llm_service")
async def llm_service_choose_handler(call: CallbackQuery) -> None:
    if isinstance(call.message, Message):
        await call.message.edit_text("Choose LLM Service:")
        await call.message.edit_reply_markup(
            reply_markup=llm_service_choose_keyboard()
        )


@router.callback_query(LLMServiceCallbackFactory.filter())
async def llm_service_chosen_handler(
    call: CallbackQuery,
    callback_data: LLMServiceCallbackFactory,
    state: FSMContext,
) -> None:
    if isinstance(call.message, Message):
        await state.update_data(service=callback_data.service)
        await llm_provider_choose_handler(call, state)


@router.callback_query(F.data == "llm_provider")
async def llm_provider_choose_handler(
    call: CallbackQuery, state: FSMContext
) -> None:
    if isinstance(call.message, Message):
        data = await state.get_data()
        await call.message.edit_text("Choose LLM Provider:")
        await call.message.edit_reply_markup(
            reply_markup=llm_provider_choose_keyboard(data["service"]),
        )


@router.callback_query(LLMProviderCallbackFactory.filter())
async def llm_provider_chosen_handler(
    call: CallbackQuery,
    callback_data: LLMProviderCallbackFactory,
    state: FSMContext,
) -> None:
    if isinstance(call.message, Message):
        await state.update_data(provider=callback_data.provider)
        await llm_model_choose_handler(call, state)


@router.callback_query(F.data == "llm_model")
async def llm_model_choose_handler(
    call: CallbackQuery,
    state: FSMContext,
) -> None:
    if isinstance(call.message, Message):
        data = await state.get_data()
        await call.message.edit_text("Choose LLM Model:")
        await call.message.edit_reply_markup(
            reply_markup=llm_model_choose_keyboard(
                data["service"], data["provider"]
            ),
        )


@router.callback_query(LLMModelCallbackFactory.filter())
async def llm_model_chosen_handler(
    call: CallbackQuery,
    callback_data: LLMModelCallbackFactory,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    if isinstance(call.message, Message):
        data = await state.get_data()
        app_user_id = await get_user_id(call.from_user.id, session)
        await set_user_llm_settings(
            app_user_id,
            session,
            llm_service=data["service"],
            llm_provider=data["provider"],
            llm_model=callback_data.model,
        )
        await call.message.edit_text(
            f"LLM Settings: {data["service"]} > "
            f"{data["provider"]} > {callback_data.model}"
        )
