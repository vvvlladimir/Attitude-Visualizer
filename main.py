import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/data", StaticFiles(directory="data"), name="data")
app.mount("/node_modules", StaticFiles(directory="node_modules"), name="node")

templates = Jinja2Templates(directory="templates")


@app.get("/")
def read_root(request: Request, name: str = "FastAPI"):
    return templates.TemplateResponse("index.html", {"request": request, "name": name})


@app.get("/list_files/")
async def list_files():
    files = os.listdir("data")
    json_files = [file for file in files if file.endswith('.json')]
    return {"files": json_files}
