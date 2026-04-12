from fastapi import APIRouter, Query

from app.api.dependencies import art_work_dep

router = APIRouter()


@router.get("/search")
async def search_artworks(
    service: art_work_dep,
    q: str = Query("", min_length=1),
    limit: int = Query(10),
    offset: int = Query(0),
) -> list[dict]:
    return await service.search_places(query=q, limit=limit, offset=offset)

@router.get("/{place_id}")
async def get_place_by_id(
    service: art_work_dep, place_id: int
):
    return await service.get_place_by_id(place_id)
