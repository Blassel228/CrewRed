import json

from httpx import AsyncClient

from app.core import settings
from app.redis.redis_client import redis_client


class ArtworkApiService:
    async def search_places(
        self, query: str = "", limit: int = 10, offset: int = 0
    ) -> list[dict]:

        cache_key = f"places:{query}:{limit}:{offset}"

        cached = await redis_client.get(cache_key)
        if cached:
            return json.loads(cached)

        async with AsyncClient(timeout=10.0) as client:
            params = {
                "q": query,
                "limit": limit,
                "offset": offset,
                "fields": "id,title,latitude,longitude,type",
            }
            resp = await client.get(
                f"{settings.ARTIC_BASE}/places/search", params=params
            )
            resp.raise_for_status()
            data = resp.json()

            places = [
                {
                    "external_id": str(item["id"]),
                    "name": item.get("title"),
                    "latitude": item.get("latitude"),
                    "longitude": item.get("longitude"),
                    "type": item.get("type"),
                }
                for item in data.get("data", [])
            ]

        await redis_client.set(cache_key, json.dumps(places), ex=3600)

        return places

    async def get_place_by_external_id(self, external_id: str) -> dict | None:
        cache_key = f"place:{external_id}"

        cached = await redis_client.get(cache_key)
        if cached:
            return json.loads(cached)

        async with AsyncClient(timeout=10.0) as client:
            resp = await client.get(f"{settings.ARTIC_BASE}/places/{external_id}")

            if resp.status_code == 404:
                return None

            resp.raise_for_status()
            data = resp.json().get("data")

        await redis_client.set(cache_key, json.dumps(data), ex=3600)
        return data
