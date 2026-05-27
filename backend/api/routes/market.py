from fastapi import APIRouter

from services.market_service import get_market_overview

router = APIRouter()


@router.get("/overview")
async def market_overview():
    results = await get_market_overview()
    return {"market_overview": results}
