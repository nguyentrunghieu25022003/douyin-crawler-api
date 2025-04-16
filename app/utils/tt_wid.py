from typing import Optional
import httpx
from http import cookies

class TtWid:
    NAME = "ttwid"
    API = "https://ttwid.bytedance.com/ttwid/union/register/"
    DATA = (
        '{"region":"cn","aid":1768,"needFid":false,"service":"www.ixigua.com",'
        '"migrate_info":{"ticket":"","source":"node"},'
        '"cbUrlProtocol":"https","union":true}'
    )

    @classmethod
    async def get_tt_wid(cls, headers: dict, proxy: str = None, **kwargs) -> Optional[str]:
        proxies = {"https": proxy} if proxy else None

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(cls.API, data=cls.DATA, headers=headers, **kwargs)
                response.raise_for_status() 
            except httpx.HTTPError as exc:
                print(f"Request failed: {exc}")
                return None

            return cls.extract(response.headers, cls.NAME)

    @staticmethod
    def extract(headers: dict, key: str) -> Optional[str]:
        if c := headers.get("Set-Cookie"):
            cookie_jar = cookies.SimpleCookie()
            cookie_jar.load(c)
            if v := cookie_jar.get(key):
                return v.value
