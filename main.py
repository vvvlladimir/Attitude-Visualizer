from fastapi import FastAPI
import tg

app = FastAPI()

@app.get("/run_script")
async def run_script():
    await tg.main()
    return {"status": "Script finished"}
