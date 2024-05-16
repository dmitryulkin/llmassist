from loguru import logger
from pydantic import BaseModel

from src.exceptions import CustomError
from src.utils.proxies.provider import ProxyProvider
from src.utils.proxies.tor_provider import TorProxyProvider
from src.utils.settings import Settings


class ProxyManager(BaseModel):
    settings: Settings
    _providers: list[ProxyProvider] = []

    async def init(self):
        logger.info("ProxyManager init...")

        # providers
        if self.settings.TOR_SOCKS5_PORT is not None:
            tor_provider = TorProxyProvider(port=self.settings.TOR_SOCKS5_PORT)
            self._init_provider(tor_provider)

        # is there any provider
        if len(self._providers) == 0:
            logger.warning("There are no active proxy providers")
        logger.info("ProxyManager init done")

    def _init_provider(self, provider: ProxyProvider):
        self._providers.append(provider)
        logger.info(f"{provider.__class__.__name__} init done")

    async def get_proxy_url(self) -> str:
        """Search preferable provider and get proxy URL"""
        provider = None
        try:
            provider = max(self._providers, key=lambda x: x.rate)
        except ValueError:
            raise CustomError("There are no proxy providers")
        return await provider.get_address()
