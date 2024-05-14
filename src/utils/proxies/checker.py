import aiohttp
from aiohttp import ClientTimeout
from aiohttp_socks import ProxyConnector


class ProxyChecker:
    async def check(self, proxy: str) -> bool:
        connector = ProxyConnector.from_url(proxy)
        async with aiohttp.ClientSession(
            connector=connector, timeout=ClientTimeout(total=10)
        ) as session:
            async with session.get("https://api.ipify.org") as response:
                return True if response.status == 200 else False
