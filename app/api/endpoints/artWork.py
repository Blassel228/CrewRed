from fastapi import APIRouter, Query

from app.api.dependencies import art_work_dep

router = APIRouter()

@router.get("/search")
async def search_artworks(
    service: art_work_dep,
    q: str = Query(..., min_length=1),
    limit: int = Query(10, ge=1, le=50),
):
    return await service.search_artworks(query=q, limit=limit)