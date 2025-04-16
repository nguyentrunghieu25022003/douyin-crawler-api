from re import compile
from typing import Tuple, List

import httpx


class DeviceId:
    NAME = "device_id"
    URL = "https://www.tiktok.com/explore"
    DEVICE_ID = compile(r'"wid":"(\d{19})"')

    @classmethod
    async def get_device_id(
        cls,
        headers: dict,
        **kwargs,
    ) -> Tuple[str, str]:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(cls.URL, headers=headers, **kwargs)
                response.raise_for_status()
            except httpx.HTTPError as exc:
                raise exc

        match = cls.DEVICE_ID.search(response.text)
        device_id = match.group(1) if match else ""

        cookie = "; ".join(
            [f"{key}={value}" for key, value in response.cookies.items()]
        )
        return device_id, cookie

    @classmethod
    async def get_device_ids(
        cls,
        headers: dict,
        number: int,
        **kwargs,
    ) -> List[Tuple[str, str]]:
        results = []
        for _ in range(number):
            result = await cls.get_device_id(headers, **kwargs)
            results.append(result)
        return results
