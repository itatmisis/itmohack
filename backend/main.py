#!/usr/bin/env python3
import random
from pathlib import Path
from typing import Optional
import json

from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.requests import Request
import uvicorn
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from backend import api
from pydantic import BaseModel

app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.parent.absolute() / "frontend" / "static"),
    name="static"
)

templates = Jinja2Templates(directory=Path(__file__).parent.parent.absolute() / "frontend" / "templates")


class ModelRequest(BaseModel):
    description: str
    organizations: Optional[str] = None
    tags: Optional[str] = None


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/get_response")
async def get_result(request: Request):
    desc = (await request.form())['description']
    embeddings = api.get_embedings(desc)
    # sorted_ids = api.get_graph_ids(embeddings)
    sampled_articles = api.get_random_articles(10)

    return templates.TemplateResponse("main.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info")
