from typing import Union
from urllib.parse import urljoin

import requests


def prepare_http_session(
    pool_connections: int,
    pool_maxsize: int,
    retry_count: int = 0,
    pool_block: bool = False,
) -> requests.Session:
    """
    Prepare http session with custom pooling. See:
    https://urllib3.readthedocs.io/en/stable/advanced-usage.html
    https://docs.python-requests.org/en/latest/api/#requests.adapters.HTTPAdapter
    """
    session = requests.Session()
    retry_conf: Union[requests.adapters.Retry, int] = (
        requests.adapters.Retry(
            total=retry_count, backoff_factor=0.3, respect_retry_after_header=False
        )
        if retry_count
        else 0
    )

    adapter = requests.adapters.HTTPAdapter(
        pool_connections=pool_connections,  # Doing all the connections to the same url
        pool_maxsize=pool_maxsize,  # Number of concurrent connections
        max_retries=retry_conf,  # Nodes are not very responsive some times
        pool_block=pool_block,
    )
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def build_full_url(base_url: str, url: str) -> str:
    """
    Combines a base URL and a relative URL into a complete URL.

    Ensures the base URL has the correct scheme (http:// or https://) and
    removes any duplicate slashes between the base URL and the relative URL.

    :param base_url: Base URL
    :param url: Relative URL
    :return: The complete URL formed by combining base_url and url.
    """
    if not base_url.startswith(("http://", "https://")):
        base_url = f"http://{base_url}/"

    base_url = base_url.rstrip("/")
    url = url.lstrip("/")

    return urljoin(f"{base_url}/", url)
