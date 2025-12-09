import asyncio
import httpx

async def async_webrequest(url, type='get', content=None, form=False):
    async with httpx.AsyncClient() as client:
        method = getattr(client, type)
        kwargs = {
            "url": url,
            "data" if form else "json": content or {},
        }
        response = await method(**kwargs)
    return response.json()
    