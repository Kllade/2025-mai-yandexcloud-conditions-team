from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from bot.utils.setup_logging import setup_logging
from bot.main import main, stop_polling
import asyncio


logger = setup_logging()



@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[dict, None]:
    global logger
    """
    Управляет жизненным циклом планировщика приложения.

    Args:
        app (FastAPI): Экземпляр приложения FastAPI.
    """

    logger.info("Начало работы приложения...")
    polling_task = asyncio.create_task(main())
    yield
    await stop_polling()
    logger.info("Завершение работы приложения...")


def create_app() -> FastAPI:
    """
    Создание и конфигурация FastAPI приложения.

    Returns:
        Сконфигурированное приложение FastAPI
    """
    app = FastAPI(
        title="Mai assistent API",
        description=(
            "Апи для работы с чат-ботом Mai assistent и его данными"
        ),
        version="1.0.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_routers(app)

    return app


def register_routers(app: FastAPI) -> None:
    """Регистрация роутеров приложения."""
    
    root_router = APIRouter()

    @root_router.get("/", tags=["root"])
    def home_page():
        return {
            "message": "Hello",
        }

    # Подключение роутеров
    app.include_router(root_router, tags=["root"])
    # app.include_router(router_auth, prefix='/auth', tags=['Auth'])
    

app = create_app()


# if __name__ == "__main__":
#     import uvicorn

#     logger.info(f"Start the application")
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
