import asyncio
import httpx

from typing import *



async def async_webrequest(url, type, content=None, form=False) -> dict:
    async with httpx.AsyncClient() as client:
        method = getattr(client, type)
        kwargs = {
            "url": url,
            "data" if form else "json": content or {},
        }
        response = await method(**kwargs)
    return response.json()
    