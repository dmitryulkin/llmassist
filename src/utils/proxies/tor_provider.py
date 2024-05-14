import random

from pydantic import PositiveInt

from src.exceptions import CustomError
from src.utils.proxies.provider import ProxyProvider
from src.utils.proxies.checker import ProxyChecker


class TorProxyProvider(ProxyProvider):
    port: PositiveInt

    def _get_address(self) -> str:
        """Use random user. It will cause each request trough
        different IP because of Tor isolation rules
        Returns:
            str: Tor's proxy address with random user's credentials
        """
        creds = str(random.randint(10000, 0x7FFFFFFF)) + ":" + "passwd"
        return f"socks5://{creds}@localhost:{self.port}"

    async def _check_address(self, address: str) -> bool:
        return await ProxyChecker().check(address)

    async def check(self) -> bool:
        addr = self._get_address()
        return await self._check_address(addr)

    async def get_address(self) -> str:
        addr = self._get_address()
        if await self._check_address(addr):
            return addr
        else:
            raise CustomError("Tor proxy address is not working")
