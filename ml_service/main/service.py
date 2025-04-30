from IPython.display import Markdown, display
import os
from yandex_cloud_ml_sdk import YCloudML
from glob import glob
from tqdm.auto import tqdm
import pandas as pd
from yandex_cloud_ml_sdk.search_indexes import (
    StaticIndexChunkingStrategy,
    HybridSearchIndexType,
    ReciprocalRankFusionIndexCombinationStrategy,
)

class Agent:
    def __init__(self, assistant=None, instruction=None, search_index=None, tools=None):

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
        if thread is not None:
            return thread
        if self.thread == None:
            self.thread = create_thread()
        return self.thread

    def __call__(self, message, thread=None):
        thread = self.get_thread(thread)
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
        return res.text

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

def upload_file():
    return sdk.files.upload('docs/docs/parsed-json/data2024.json', ttl_days=1, expiration_policy="static")

def printx(string):
    display(Markdown(string))

folder_id = 'b1gst3c7cskk2big5fqn'
api_key = 'AQVNzzJielnSayrAOlQWlxDMK49OShvzdqtUQdAp'

sdk = YCloudML(folder_id=folder_id, auth=api_key)
model = sdk.models.completions("yandexgpt", model_version="rc")
g = upload_file()
op = sdk.search_indexes.create_deferred(
    g,
    index_type=HybridSearchIndexType(
        chunking_strategy=StaticIndexChunkingStrategy(
            max_chunk_size_tokens=1000, chunk_overlap_tokens=100
        ),
        combination_strategy=ReciprocalRankFusionIndexCombinationStrategy(),
    ),
)
index = op.wait()
op = sdk.search_indexes.create_deferred(
    g,
    index_type=HybridSearchIndexType(
        chunking_strategy=StaticIndexChunkingStrategy(
            max_chunk_size_tokens=1000, chunk_overlap_tokens=100
        ),
        combination_strategy=ReciprocalRankFusionIndexCombinationStrategy(),
    ),
)
index = op.wait()
instruction = """
Представь что ты являешься оператором приемной комиссии в МАИ, и тебе задают вопросы разного вида. Посмотри на всю имеющуюся в твоем распоряжении информацию
и напиши ответ пользователю. Если что-то непонятно, то лучше уточни информацию. Остальные вопросы, которые не связаны с поступлением или с вопросами о вузе, игнорируй их и не пиши про них ничего
у пользователя. 
"""

agent = Agent(
    instruction=instruction,
    search_index=index
)