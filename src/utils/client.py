import aiohttp
import ssl


def get_session():
    """Creates an aiohhtp session.

    Returns:
        obj: Aiohttp client session.
    """
    ssl_ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE
    conn = aiohttp.TCPConnector(ssl=ssl_ctx)
    return aiohttp.ClientSession(connector=conn)
