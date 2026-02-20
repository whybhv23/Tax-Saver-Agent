from fastapi import APIRouter, Request
from app.utils.agent import tax_saver_agent

router = APIRouter()

@router.post("/generate-report")
async def generate_report(request: Request):
    user_data = await request.json()
    report = tax_saver_agent(user_data)
    return {"report": report}