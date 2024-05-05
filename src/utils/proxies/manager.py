from pydantic import BaseModel

from src.exceptions import CustomError
from src.context import ctx
from src.utils.loggers import get_logger
from src.utils.proxies.provider import ProxyProvider
from src.utils.proxies.tor_provider import TorProxyProvider

logger = get_logger(__name__)


class ProxyManager(BaseModel):
    providers: list[ProxyProvider] = []

    def _config_tor_provider(self) -> None:
        TOR_PORT = ctx.settings.TOR_SOCKS5_PORT
        if not TOR_PORT:
            raise CustomError("TOR_SOCKS5_PORT is None")
        tor_provider: TorProxyProvider = TorProxyProvider(port=TOR_PORT)
        if tor_provider.is_alive():
            self.providers.append(tor_provider)
            logger.info("Init Tor proxy is done")
        else:
            raise CustomError("Tor provider is not alive")

    def __init__(self) -> None:
        logger.info("Init ProxyManager")
        super().__init__()  # BaseModel functionality
        if not ctx.settings:
            raise CustomError("ctx.settings is None")
        # initialize Tor proxy provider
        if ctx.settings.USE_TOR:
            logger.info("Init Tor provider on USE_TOR=True")
            try:
                self._config_tor_provider()
            except Exception as e:
                logger.error(
                    "Init Tor provider failed: %s",
                    repr(e),
                )
        # is there any provider
        if len(self.providers) == 0:
            logger.warn("There are no active proxy providers")
        logger.info("Init ProxyManager done")

    def get_provider(self) -> ProxyProvider:
        return max(self.providers, key=lambda x: x.rate)
