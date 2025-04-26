import platform
import multiprocessing
import random
import psutil

from urllib.parse import urlencode
from ..utils.a_bogus import ABogus

COMMON_PARAMS = {
    "device_platform": "webapp",
    "aid": "6383",
    "channel": "channel_pc_web",
    "pc_client_type": "1",
    "pc_libra_divert": "Windows",
    "support_h265": "1",
    "support_dash": "1",
    "version_code": "170400",
    "version_name": "17.4.0",
    "cookie_enabled": "true",
    "browser_language": "en-US",
    "browser_platform": "Win32",
    "browser_name": "Chrome",
    "browser_version": "135.0.0.0",
    "browser_online": "true",
    "engine_name": "Blink",
    "engine_version": "135.0.0.0",
    "platform": "PC",
    "downlink": "10",
    "effective_type": "4g",
    "round_trip_time": "50",
}

def get_dynamic_params():
    cpu_cores = multiprocessing.cpu_count()

    if psutil:
        ram_gb = int(psutil.virtual_memory().total / (1024 ** 3))
    else:
        ram_gb = random.choice([4, 8, 16, 32])
    common_res = [(1920,1080), (1536,864), (1366,768), (1440,900)]
    width, height = random.choice(common_res)

    os_name = platform.system()
    os_version = platform.release()

    return {
        "cpu_core_num": str(cpu_cores),
        "device_memory": str(ram_gb),
        "screen_width": str(width),
        "screen_height": str(height),
        "os_name": os_name,
        "os_version": os_version,
    }

def build_url(base_url: str, extra_params: dict) -> str:
    params = {}
    params.update(COMMON_PARAMS)
    params.update(get_dynamic_params())
    params.update(extra_params)

    query = urlencode(params)
    bogus = ABogus().get_value(query)
    return f"{base_url}?{query}&a_bogus={bogus}"

def build_douyin_feed_url(
    refresh_index: int = 1,
    count: int = 10,
    webid: str = "",
    verifyFp: str = "",
    fp: str = "",
    msToken: str = "",
) -> str:
    base = "https://www.douyin.com/aweme/v1/web/tab/feed/"
    extra = {
        "count": count,
        "refresh_index": refresh_index,
        "video_type_select": "1",
        "is_client": "false",
        "is_dash_user": "1",
        "is_auto_play": "0",
        "is_full_screen": "0",
        "is_full_webscreen": "0",
        "is_mute": "0",
        "is_speed": "1",
        "is_visible": "1",
        "related_recommend": "1",
        "webid": webid,
        "verifyFp": verifyFp,
        "fp": fp,
        "msToken": msToken,
    }
    return build_url(base, extra)

def build_douyin_wallpaper_url(
    cursor: int = 0,
    count: int = 10,
    webid: str = "",
    msToken: str = "",
    uifid: str = "",
    verify_fp: str = "",
    fp: str = ""
) -> str:
    base = "https://www.douyin.com/aweme/v1/web/wallpaper/item/"
    extra = {
        "version": "2",
        "need_aweme_image": "true",
        "cursor": cursor,
        "count": count,
        "sort_type": "0",
        "video_type_select": "1",
        "update_version_code": "170400",
        "webid": webid,
        "uifid": uifid,
        "verifyFp": verify_fp,
        "fp": fp,
        "msToken": msToken,
    }
    return build_url(base, extra)

def build_douyin_vlog_url(
    module_id: str = "3003101",
    tag_id: str = "300216",
    refresh_index: int = 1,
    count: int = 20,
    webid: str = "",
    verifyFp: str = "",
    fp: str = "",
    msToken: str = "",
    uifid: str = ""
) -> str:
    base = "https://www.douyin.com/aweme/v1/web/module/feed/"
    extra = {
        "module_id": module_id,
        "tag_id": tag_id,
        "count": count,
        "refresh_index": refresh_index,
        "refer_type": "10",
        "refer_id": "",
        "presented_ids": "",
        "filterGids": "",
        "awemePcRecRawData": '{"is_xigua_user":0,"is_client":false}',
        "Seo-Flag": "0",
        "install_time": "1743829679",
        "webid": webid,
        "verifyFp": verifyFp,
        "fp": fp,
        "msToken": msToken,
        "uifid": uifid
    }
    return build_url(base, extra)