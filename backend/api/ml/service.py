import aiohttp
from bot.core.config import settings

class MLService:
    def __init__(self):
        self.base_url = settings.ML_SERVER_URL

    async def get_answer(self, question: str) -> str:
        """Get answer from ML server for the given question."""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/answer",
                json={"question": question}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data["answer"]
                else:
                    return "Извините, произошла ошибка при получении ответа. Попробуйте позже."

ml_service = MLService() 