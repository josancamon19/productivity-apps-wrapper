from typing import Optional, Any
from fastapi import FastAPI, Request
import json

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/receive")
def receive_data(request: Request):
    # print(json.dumps(request.body(), indent=4))
    print(request.base_url.hostname)
    return {'nice': True}


@app.get("/receive")
def receive_data():
    print('Received')
    return {'valid': True}
