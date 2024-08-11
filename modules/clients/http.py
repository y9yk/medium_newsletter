import aiohttp
import async_timeout

from config import settings


async def make_request(
    url: str,
    method: str,
    data: dict = None,
    headers: dict = None,
    is_json_resp: bool = False,
):
    if not data:
        data = {}

    with async_timeout.timeout(settings.TIMEOUT):
        async with aiohttp.ClientSession() as session:
            request = getattr(session, method)
            async with request(url, json=data, headers=headers) as response:
                if is_json_resp:
                    data = await response.json()
                else:
                    data = await response.text()
                return (data, response.status)
