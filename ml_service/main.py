from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from service.service import Agent, instruction, index

class Data(BaseModel):
    text: str
    thread_id: str | None = None

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/question")
async def promt(data: Data):

    agent = Agent(
        thread_id=data.thread_id,
        instruction=instruction,
        search_index=index,
    )
    res = agent(data.text, data.thread_id)


    return {"answer": res[0], "thread_id": res[1]}



if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8001, workers=3)