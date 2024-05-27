from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.services import srv


def settings_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="LLM", callback_data="llm_settings")],
        [InlineKeyboardButton(text="Cancel", callback_data="cancel")],
    ]
    keyboard = InlineKeyboardBuilder(markup=buttons)
    return keyboard.as_markup()


def llm_settings_keyboard(
    llm_service: str | None, llm_provider: str | None
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="Services", callback_data="llm_service")
    if llm_service:
        keyboard.button(text="Providers", callback_data="llm_provider")
    if llm_provider:
        keyboard.button(text="Model", callback_data="llm_model")
    keyboard.button(text="Cancel", callback_data="cancel")
    keyboard.adjust(1)
    return keyboard.as_markup()


class LLMServiceCallbackFactory(CallbackData, prefix="llm_service"):
    service: str


def llm_service_choose_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    for name in srv.llm.services:
        keyboard.button(
            text=name,
            callback_data=LLMServiceCallbackFactory(service=name),
        )
    keyboard.button(text="Cancel", callback_data="cancel")
    keyboard.adjust(1)
    return keyboard.as_markup()


class LLMProviderCallbackFactory(CallbackData, prefix="llm_provider"):
    service: str
    provider: str


def llm_provider_choose_keyboard(llm_service: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    providers = srv.llm.services[llm_service].get_providers()
    for provider in providers:
        keyboard.button(
            text=provider,
            callback_data=LLMProviderCallbackFactory(
                service=llm_service, provider=provider
            ),
        )
    keyboard.button(text="Cancel", callback_data="cancel")
    return keyboard.as_markup()


class LLMModelCallbackFactory(CallbackData, prefix="llm_model"):
    service: str
    provider: str
    model: str


def llm_model_choose_keyboard(
    llm_service: str, llm_provider: str
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    models = srv.llm.services[llm_service].get_provider_models(llm_provider)
    for model in models:
        keyboard.button(
            text=model,
            callback_data=LLMModelCallbackFactory(
                service=llm_service, provider=llm_provider, model=model
            ),
        )
    keyboard.button(text="Cancel", callback_data="cancel")
    keyboard.adjust(1)
    return keyboard.as_markup()
