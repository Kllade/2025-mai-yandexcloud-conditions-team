from fastapi import FastAPI
from pydantic import BaseModel

class Data(BaseModel):
    text: str

app = FastAPI()

@app.post("/")
def promt(data: Data):
    print(data.text)
    return {"message": "Строка успешно выведена в консоль"}