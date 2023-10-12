from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/data", StaticFiles(directory="data"), name="data")
app.mount("/chart.js", StaticFiles(directory="chart.js"), name="chart.js")

templates = Jinja2Templates(directory="templates")

@app.get("/")
def read_root(request: Request, name: str = "FastAPI"):
    return templates.TemplateResponse("index.html", {"request": request, "name": name})
