import os
from pathlib import Path

from fastapi import FastAPI
from fastapi import Form, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from tg import *

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/data", StaticFiles(directory="data"), name="data")
app.mount("/node_modules", StaticFiles(directory="node_modules"), name="node")

templates = Jinja2Templates(directory="templates")

data_directory = Path("/data/")


def read_from_file():
    with open("config.json", "r") as file:
        return json.load(file)


@app.get("/")
def read_root(request: Request, name: str = "FastAPI"):
    data = read_from_file()
    return templates.TemplateResponse("index.html", {"request": request, "name": name, "data": data})


@app.post("/take_reactions/")
async def submit_form(
        telegram_id: int = Form(...),
        telegram_hash: str = Form(...),
        post_limit: int = Form(...),
        post_offset: int = Form(...),
        channel_link: str = Form(...),

):
    data = {
        "telegram_id": telegram_id,
        "telegram_hash": telegram_hash,
        "post_limit": post_limit,
        "post_offset": post_offset,
        "channel_link": channel_link
    }
    with open("config.json", "w") as file:
        json.dump(data, file)

    await main()

    response = Response(status_code=302)
    response.headers["Location"] = "/"  # URL вашей главной страницы
    return response


@app.get("/list_files/")
async def list_files():
    files = os.listdir("data")
    json_files = [file for file in files if file.endswith('.json')]
    return {"files": json_files}


@app.get("/files/")
async def get_files():
    files = [f.name for f in data_directory.iterdir() if f.is_file()]
    return {"files": files}
