from aiogram import Router


def get_handlers_router() -> Router:
    from . import menu, start

    router = Router()
    router.include_router(start.router)
    router.include_router(menu.router)
    

    return router