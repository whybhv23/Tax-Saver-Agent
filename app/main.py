from fastapi import FastAPI
import uvicorn
from app.routers import tax_saver
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI()

app.include_router(tax_saver.router, tags=["tax-saver-agent"], prefix="/tax-saver-agent")
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

@app.get("/", include_in_schema=False)
async def custom_index():
    index_path = os.path.join(os.path.dirname(__file__), "..", "static", "indexcopy.html")
    return FileResponse(index_path)

@app.get("/health")
async def root():
    return {"message": "API is working fine."}

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app", host="127.0.0.1", port=8000, log_level="info", reload=True
    )