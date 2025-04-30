import aiohttp
from bot.core.config import settings
from pydantic import BaseModel
import logging
logger = logging.getLogger(__name__)

class Data(BaseModel):
    text: str

class MLService:
    def __init__(self):
        self.base_url = settings.ML_SERVER_URL

    async def get_answer(self, question: str) -> str:
        """Get answer from ML server for the given question."""
        payload = Data(text=question).model_dump()
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}",
                json=payload
            ) as response:
                if response.status == 200:
                    logger.info(f"data: {response}")
                    data = await response.json()
                    logger.info(f"data: {data}")
                    return data["answer"]
                else:
                    return "Извините, произошла ошибка при получении ответа. Попробуйте позже."

ml_service = MLService() 