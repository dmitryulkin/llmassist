from aiogram import Router


def get_handlers_router() -> Router:
    from . import messages, settings

    router = Router()
    # !!! order matters
    router.include_router(settings.router)
    router.include_router(messages.router)

    return router
