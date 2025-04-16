from urllib.parse import urlencode
from .utils.a_bogus import ABogus

from urllib.parse import urlencode
from .utils.a_bogus import ABogus

def build_douyin_feed_url(
    refresh_index: int = 1,
    count: int = 10,
    webid: str = "",
    msToken: str = "",
):
    base_url = "https://www.douyin.com/aweme/v1/web/tab/feed/"
    
    params = {
        "device_platform": "webapp",
        "aid": "6383",
        "channel": "channel_pc_web",
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
        "pc_client_type": "1",
        "pc_libra_divert": "Windows",
        "support_h265": "1",
        "support_dash": "1",
        "version_code": "170400",
        "version_name": "17.4.0",
        "cookie_enabled": "true",
        "screen_width": "1536",
        "screen_height": "864",
        "browser_language": "en-US",
        "browser_platform": "Win32",
        "browser_name": "Chrome",
        "browser_version": "135.0.0.0",
        "browser_online": "true",
        "engine_name": "Blink",
        "engine_version": "135.0.0.0",
        "os_name": "Windows",
        "os_version": "10",
        "cpu_core_num": "8",
        "device_memory": "8",
        "platform": "PC",
        "downlink": "10",
        "effective_type": "4g",
        "round_trip_time": "50",
        "webid": webid,
        "msToken": msToken,
    }

    query_string = urlencode(params)
    bogus = ABogus().get_value(query_string)
    full_url = f"{base_url}?{query_string}&a_bogus={bogus}"
    return full_url

def build_douyin_wallpaper_url(
    cursor: int = 0,
    count: int = 4,
    webid: str = "",
    msToken: str = "",
    uifid: str = "",
    verify_fp: str = "",
    fp: str = ""
):
    base_url = "https://www.douyin.com/aweme/v1/web/wallpaper/item/"

    params = {
        "version": "2",
        "need_aweme_image": "true",
        "device_platform": "webapp",
        "aid": "6383",
        "channel": "channel_pc_web",
        "cursor": cursor,
        "count": count,
        "sort_type": "0",
        "video_type_select": "1",
        "update_version_code": "170400",
        "pc_client_type": "1",
        "pc_libra_divert": "Windows",
        "support_h265": "1",
        "support_dash": "1",
        "version_code": "170400",
        "version_name": "17.4.0",
        "cookie_enabled": "true",
        "screen_width": "1536",
        "screen_height": "864",
        "browser_language": "en-US",
        "browser_platform": "Win32",
        "browser_name": "Chrome",
        "browser_version": "135.0.0.0",
        "browser_online": "true",
        "engine_name": "Blink",
        "engine_version": "135.0.0.0",
        "os_name": "Windows",
        "os_version": "10",
        "cpu_core_num": "8",
        "device_memory": "8",
        "platform": "PC",
        "downlink": "10",
        "effective_type": "4g",
        "round_trip_time": "50",
        "webid": webid,
        "uifid": uifid,
        "verifyFp": verify_fp,
        "fp": fp,
        "msToken": msToken,
    }

    query = urlencode(params)
    bogus = ABogus().get_value(query)
    return f"{base_url}?{query}&a_bogus={bogus}"