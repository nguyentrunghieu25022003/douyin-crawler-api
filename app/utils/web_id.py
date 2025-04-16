from typing import Optional
import httpx

class WebId:
    NAME = "webid"
    API = "https://mcs.zijieapi.com/webid"
    PARAMS = {"aid": "6383", "sdk_version": "5.1.18_zip", "device_platform": "web"}

    @classmethod
    async def get_web_id(cls, headers: dict, proxy: str = None, **kwargs) -> Optional[str]:
        user_agent = headers.get("User-Agent")
        data = (
            f'{{"app_id":6383,"url":"https://www.douyin.com/","user_agent":"{user_agent}",'
            f'"referer":"https://www.douyin.com/","user_unique_id":""}}'
        )
        proxies = {"https": proxy} if proxy else None

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    cls.API,
                    params=cls.PARAMS,
                    data=data,
                    headers=headers,
                    **kwargs,
                )
                response.raise_for_status()
            except httpx.HTTPError as exc:
                print(f"HTTP error: {exc}")
                return None
            json_resp = response.json()
            return json_resp.get("web_id")
