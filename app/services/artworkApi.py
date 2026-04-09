import httpx

from app.core import settings


class ArtworkApiService:
    async def search_artworks(self, query: str, limit: int = 10):
        async with httpx.AsyncClient(timeout=10.0) as client:
            params = {"q": query, "limit": limit, "fields": "id,title,artist_display,place_of_origin"}
            resp = await client.get(f"{settings.ARTIC_BASE}/artworks/search", params=params)
            resp.raise_for_status()
            data = resp.json()

            return [
                {
                    "external_id": str(item["id"]),
                    "name": item.get("title", "Untitled"),
                    "location": item.get("place_of_origin"),
                    "artist": item.get("artist_display"),
                }
                for item in data.get("data", [])
            ]