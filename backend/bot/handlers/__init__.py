from aiogram import Router
from .start import router as start_router
from .on_click import router as on_click_router
from .reactions import router as reactions_router

router = Router(name="main_router")
router.include_router(start_router)
router.include_router(on_click_router)
router.include_router(reactions_router)


def get_handlers_router() -> Router:
    from . import menu, start

    router = Router()
    router.include_router(start.router)
    router.include_router(menu.router)
    

    return router