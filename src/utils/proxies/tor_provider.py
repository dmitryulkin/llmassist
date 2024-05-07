import random

from src.utils.proxies.provider import ProxyProvider


class TorProxyProvider(ProxyProvider):
    port: int

    def get_address(self) -> str:
        """Use random user. It will cause each request trough
        different IP because of Tor isolation rules
        Returns:
            str: Tor's proxy address with random user's credentials
        """
        creds = str(random.randint(10000, 0x7FFFFFFF)) + ":" + "passwd"
        return f"socks5://{creds}@localhost:{self.port}"

    def is_alive(self) -> bool:
        try:
            raise NotImplementedError
        except Exception:
            return False
