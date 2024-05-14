from loguru import logger
from pydantic import BaseModel

from src.services import srv
from src.utils.proxies.provider import ProxyProvider
from src.utils.proxies.tor_provider import TorProxyProvider


class ProxyManager(BaseModel):
    providers: list[ProxyProvider] = []

    async def init(self):
        logger.info("ProxyManager init...")

        # providers
        if srv.settings.TOR_SOCKS5_PORT is not None:
            tor_provider = TorProxyProvider(port=srv.settings.TOR_SOCKS5_PORT)
            self._init_provider(tor_provider)

        # is there any provider
        if len(self.providers) == 0:
            logger.warning("There are no active proxy providers")
        logger.info("ProxyManager init done")

    def _init_provider(self, provider: ProxyProvider):
        self.providers.append(provider)
        logger.info(f"{provider.__class__.__name__} init done")

    def get_provider(self) -> ProxyProvider:
        return max(self.providers, key=lambda x: x.rate)
