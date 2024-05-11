from loguru import logger
from pydantic import BaseModel

from src.services import srv
from src.utils.proxies.provider import ProxyProvider
from src.utils.proxies.tor_provider import TorProxyProvider


class ProxyManager(BaseModel):
    providers: list[ProxyProvider] = []

    def _config_tor_provider(self) -> None:
        TOR_PORT = srv.settings.TOR_SOCKS5_PORT
        if not TOR_PORT:
            return
        logger.info("Tor provider init...")
        tor_provider: TorProxyProvider = TorProxyProvider(port=TOR_PORT)
        if tor_provider.is_alive():
            self.providers.append(tor_provider)
            logger.info("Tor provider init done")
        else:
            logger.error("Tor provider init failed: is not alive")

    def __init__(self) -> None:
        logger.info("ProxyManager init...")
        super().__init__()  # BaseModel functionality

        self._config_tor_provider()

        # is there any provider
        if len(self.providers) == 0:
            logger.warning("There are no active proxy providers")
        logger.info("ProxyManager init done")

    def get_provider(self) -> ProxyProvider:
        return max(self.providers, key=lambda x: x.rate)
