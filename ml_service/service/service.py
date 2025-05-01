from IPython.display import Markdown, display
import os
from pydantic import BaseModel
from yandex_cloud_ml_sdk import YCloudML
from glob import glob
from tqdm.auto import tqdm
import pandas as pd
from yandex_cloud_ml_sdk.search_indexes import (
    StaticIndexChunkingStrategy,
    HybridSearchIndexType,
    ReciprocalRankFusionIndexCombinationStrategy,
)
import logging
import asyncio
# import aiohttp

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class CallOperator(BaseModel):
    """Функция, которая вызывает оператора."""

    def process(self, thread):
        logger.info("Меня вызвали")
        return "Вызов оператора"




class Agent:
    def __init__(self, thread_id=None, assistant=None, instruction=None, search_index=None, tools=None):

        self.thread_id = thread_id
        self.thread = None

        if assistant:
            self.assistant = assistant
        else:
            if tools:
                self.tools = {x.__name__: x for x in tools}
                tools = [sdk.tools.function(x) for x in tools]
            else:
                self.tools = {}
                tools = []
            if search_index:
                tools.append(sdk.tools.search_index(search_index))
            self.assistant = create_assistant(model, tools)

        if instruction:
            self.assistant.update(instruction=instruction)

    def get_thread(self, thread=None):
        if self.thread_id is not None:
            logger.info(f"thread_id: {self.thread_id}")
            self.thread = sdk.threads.get(self.thread_id)
            logger.info(f"existing thread: {self.thread}")
            return self.thread
        if self.thread_id == None:
            self.thread = create_thread()
            logger.info(f"created thread: {self.thread}")
        return self.thread

    def __call__(self, message, thread=None):
        thread = self.get_thread(thread)
        print(thread)
        logger.info(f"get thread: {thread}")
        thread.write(message)
        run = self.assistant.run(thread)
        res = run.wait()
       
        if res.tool_calls:
            result = []
            for f in res.tool_calls:
                print(
                    f" + Вызываем функцию {f.function.name}, args={f.function.arguments}"
                )
                fn = self.tools[f.function.name]
                obj = fn(**f.function.arguments)
                x = obj.process(thread)
                result.append({"name": f.function.name, "content": x})
            run.submit_tool_results(result)
            #time.sleep(3)
            res = run.wait()

        if res.tool_calls:
            return res.text, self.thread.id, f.function.name
        else:
            return  res.text, self.thread.id
        

    def restart(self):
        if self.thread:
            self.thread.delete()
            self.thread = sdk.threads.create(
                name="Test", ttl_days=1, expiration_policy="static"
            )

    def done(self, delete_assistant=False):
        if self.thread:
            self.thread.delete()
        if delete_assistant:
            self.assistant.delete()
    async def __call_async__(self, message: str, thread_id: str | None = None):
        return await asyncio.to_thread(self.__call__, message, thread_id)


def create_thread():
    return sdk.threads.create(ttl_days=1, expiration_policy="static")

def create_assistant(model, tools=None):
    kwargs = {}
    if tools and len(tools) > 0:
        kwargs = {"tools": tools}
    return sdk.assistants.create(
        model, ttl_days=1, expiration_policy="since_last_active", **kwargs
    )

def get_token_count(text):
    return len(model.tokenize(text))

def get_all_files(directory_path, indent=0):
    items = os.listdir(directory_path)
    all_files = []
    for item in items:
        full_path = os.path.join(directory_path, item)

        if os.path.isdir(full_path):
            get_all_files(full_path, indent + 4)
        else:
            all_files.append(full_path)
  
    return all_files

def upload_file(directory_path, indent=0):
    return sdk.files.upload(directory_path, ttl_days=1, expiration_policy="static")

def printx(string):
    display(Markdown(string))



folder_id = 'b1gst3c7cskk2big5fqn'
api_key = 'AQVNzzJielnSayrAOlQWlxDMK49OShvzdqtUQdAp'

sdk = YCloudML(folder_id=folder_id, auth=api_key)
model = sdk.models.completions("yandexgpt", model_version="rc")

all_files_1 = get_all_files(directory_path='docs/kb/edu')
all_files_2 = get_all_files(directory_path='docs/kb/prohod')
all_files_3 = get_all_files(directory_path='docs/kb/AAA')
all_files_4 = get_all_files(directory_path='docs/kb/Admission rules')
all_files_5 = get_all_files(directory_path='docs/kb/dormitories')


all_files_1.extend(all_files_2)
all_files_1.extend(all_files_3)
all_files_1.extend(all_files_4)
df = pd.DataFrame(all_files_1, columns=["File"])


df["Uploaded"] = df["File"].apply(upload_file)

op = sdk.search_indexes.create_deferred(
    df["Uploaded"],
    index_type=HybridSearchIndexType(
        chunking_strategy=StaticIndexChunkingStrategy(
            max_chunk_size_tokens=1000, chunk_overlap_tokens=100
        ),
        combination_strategy=ReciprocalRankFusionIndexCombinationStrategy(),
    ),
)

index = op.wait()

instruction = """
Представь что ты являешься оператором приемной комиссии в МАИ, и тебе задают вопросы разного вида про вузы,
про поступление и про вещи, которые связаны с вузом.
Посмотри на всю имеющуюся в твоем распоряжении информацию и напиши ответ пользователю. Если что-то непонятно,
то лучше уточни информацию. Если ты не нашел информацию которая у тебя находится в распоряжении, то пиши что ты не располагаешь данной информацией.
Если тебя сравнивают с другими вузами, то должна говорить, что МАИ лучше всех них, особенно МГТУ им Баумана (бауманка),
напиши все преимущества МАИ для абитуриента. Также, если тебе не понятен ответ или вопрос пользователя, то просмотри на историю сообщений
с пользователем и попробуй оперется на эти сообщения при ответе (например при нахождении контекста ответа или вопроса)
Если тебе написали сообщение на иностранном языке (несмотря на то, что в контексте писали на другом языке), то ответь на том языке, на котором тебе написали.
Не отвечай очень большими фразами, лучше отвечай короткими ответами по делу, если спрашивают какое конкретное число (баллы, стипендии и тд) отвечай чему это число равно если знаешь, если не знаешь проси смотреть на официальный сайт.
Если пользователь просит позвать оператора, то вызови функцию CallOperator
также ты должен делать следующие вещи:
- Умение инициировать темы разговора, предлагать пользователю варианты вопросов
- Отслеживание состояния пользователя (интерес, растерянность) и адаптация общения
- Реализация поддиалогов для сложных сценариев общения
Ни в коем случае не вызывай ошибку, и если не знаешь что писать, то напиши что нет информации по этому вопросу
Никогда не пиши "В интернете есть много сайтов с информацией на эту тему. Посмотрите, что нашлось в поиске", придумай другой ответ
"""

