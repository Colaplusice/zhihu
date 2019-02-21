HEADERS = {
    "Connection": "keep-alive",
    "Host": "www.zhihu.com",
    "Referer": "https://www.zhihu.com/",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
}
username = "18340071291"
password = "f12580f"
LOGIN_URL = "https://www.zhihu.com/signup"
LOGIN_API = "https://www.zhihu.com/api/v3/oauth/sign_in"
begin_url = "https://www.zhihu.com/people/fan-jia-liang-57/following"
FORM_DATA = {
    "client_id": "c3cef7c66a1843f8b3a9e6a1e3160e20",
    "grant_type": "password",
    "source": "com.zhihu.web",
    "username": "",
    "password": "",
    # 改为'cn'是倒立汉字验证码
    "lang": "en",
    "ref_source": "homepage",
}
