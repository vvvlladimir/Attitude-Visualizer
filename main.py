from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi import Form, Response
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from tg import *

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/data", StaticFiles(directory="data"), name="data")
app.mount("/favicon", StaticFiles(directory="favicon"), name="favicon")

if Path("node_modules").exists() and Path("node_modules").is_dir():
    app.mount("/node_modules", StaticFiles(directory="node_modules"), name="node")

templates = Jinja2Templates(directory="templates")
data_folder = Path("data")


def read_from_file():
    with open("config.json", "r") as file:
        return json.load(file)


def get_json_files_array():
    json_files = [file.name for file in data_folder.iterdir() if file.is_file() and file.suffix == ".json"]
    return json_files[:4]


@app.get("/")
def read_root(request: Request, name: str = "Visualiser"):
    config = read_from_file()
    json_files = get_json_files_array()
    return templates.TemplateResponse("index.html",
                                      {"request": request, "name": name, "config": config, "files": json_files})


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
    response.headers["Location"] = "/"
    return response


@app.get("/list_files/")
async def list_files():
    json_files = get_json_files_array()
    files = sorted(data_folder.glob('*.json'), key=lambda x: x.stat().st_mtime, reverse=True)

    if not files:
        return {"files": json_files,
                "date": "00.00.0000",
                "time": "00:00",
                }

    with files[0].open('r') as f:
        data = json.load(f)

    return {
        "files": json_files,
        "date": data["date"],
        "time": data["time"]
    }


@app.get("/download/{file_name}")
async def download_file(file_name: str):
    file_path = data_folder / file_name
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, filename=file_name, media_type="application/octet-stream")


@app.delete("/delete/{file_name}")
async def delete_file(file_name: str):
    file_path = data_folder / file_name
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    file_path.unlink()
    return {"status": "success", "message": f"Deleted {file_name}"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
