import base64
import hashlib
import hmac
import json
from logs import logger
import re
import threading
import time
from http import cookiejar
from urllib.parse import urlencode

import execjs
import requests
from PIL import Image

from configs import LOGIN_URL, LOGIN_API, FORM_DATA, HEADERS


class ZhihuDownloader(object):
    def __init__(self):
        self.login_url = LOGIN_URL
        self.login_api = LOGIN_API
        self.login_data = FORM_DATA.copy()
        self.session = requests.session()
        self.session.headers = HEADERS.copy()
        self.session.cookies = cookiejar.LWPCookieJar(filename="./cookies.txt")

    @staticmethod
    def _encrypt(form_data: dict):
        with open("./encrypt.js") as f:
            js = execjs.compile(f.read())
            return js.call("Q", urlencode(form_data))

    def login(self, username=None, password=None, load_cookies=True):
        """
        模拟登录知乎
        :param username: 登录手机号
        :param password: 登录密码
        :param load_cookies: 是否读取上次保存的 Cookies
        :return: bool
        """
        if load_cookies and self.load_cookies():
            if self.check_login():
                print("登录信息从cookie获取,已登录")
                return True
            else:
                print("cookie 失效")
                self.session.cookies.clear()
        headers = self.session.headers.copy()
        headers.update(
            {
                "accept-encoding": "gzip, deflate, br",
                "content-type": "application/x-www-form-urlencoded",
                "X-Xsrftoken": self._get_token(),
                # update
                "x-zse-83": "3_1.1",
            }
        )
        # return
        username, password = self._check_user_pass(username, password)
        self.login_data.update({"username": username, "password": password})
        timestamp = str(int(time.time() * 1000))
        self.login_data.update(
            {
                "captcha": self._get_captcha(headers),
                "timestamp": timestamp,
                "signature": self._get_signature(timestamp),
            }
        )
        # should  update encrypt data
        resp = self.session.post(
            self.login_api, data=self._encrypt(self.login_data), headers=headers
        )
        if "error" in resp.text:
            print(resp.text)
            print(re.findall(r'"message":"(.+?)"', resp.text)[0])
        elif self.check_login():
            return True
        print("登录失败")
        return False

    def load_cookies(self):
        """
        读取 Cookies 文件加载到 Session
        :return: bool
        """
        try:
            self.session.cookies.load(ignore_discard=True)
            return True
        except IOError:
            return False

    def check_login(self):
        """
        检查登录状态，访问登录页面出现跳转则是已登录，
        如登录成功保存当前 Cookies
        :return: bool
        """
        resp = self.session.get(self.login_url, allow_redirects=False)
        if resp.status_code == 302:
            self.session.cookies.save()
            print("登录成功")
            return True
        return False

    def _get_token(self):
        """
        从登录页面获取 token
        :return:
        """
        resp = self.session.get(self.login_url)
        token = re.findall(r"_xsrf=([\w|-]+)", resp.headers.get("Set-Cookie"))[0]
        print("token:", token)
        return token

    def _get_captcha(self, lang: str):
        """
        请求验证码的 API 接口，无论是否需要验证码都需要请求一次
        如果需要验证码会返回图片的 base64 编码
        根据 lang 参数匹配验证码，需要人工输入
        :param lang: 返回验证码的语言(en/cn)
        :return: 验证码的 POST 参数
        """
        if lang == "cn":
            api = "https://www.zhihu.com/api/v3/oauth/captcha?lang=cn"
        else:
            api = "https://www.zhihu.com/api/v3/oauth/captcha?lang=en"
        resp = self.session.get(api)
        show_captcha = re.search(r"true", resp.text)

        if show_captcha:
            put_resp = self.session.put(api)
            json_data = json.loads(put_resp.text)
            img_base64 = json_data["img_base64"].replace(r"\n", "")
            with open("./captcha.jpg", "wb") as f:
                f.write(base64.b64decode(img_base64))
            img = Image.open("./captcha.jpg")
            if lang == "cn":
                import matplotlib.pyplot as plt

                plt.imshow(img)
                print("点击所有倒立的汉字，在命令行中按回车提交")
                points = plt.ginput(7)
                capt = json.dumps(
                    {
                        "img_size": [200, 44],
                        "input_points": [[i[0] / 2, i[1] / 2] for i in points],
                    }
                )
            else:
                img_thread = threading.Thread(target=img.show, daemon=True)
                img_thread.start()
                capt = input("请输入图片里的验证码：")
            # 这里必须先把参数 POST 验证码接口
            self.session.post(api, data={"input_text": capt})
            return capt
        return ""

    def _get_signature(self, timestamp):
        """
        通过 Hmac 算法计算返回签名
        实际是几个固定字符串加时间戳
        :param timestamp: 时间戳
        :return: 签名
        """
        ha = hmac.new(b"d1b964811afb40118a12068ff74a12f4", digestmod=hashlib.sha1)
        grant_type = self.login_data["grant_type"]
        client_id = self.login_data["client_id"]
        source = self.login_data["source"]
        ha.update(bytes((grant_type + client_id + source + timestamp), "utf-8"))
        return ha.hexdigest()

    def _check_user_pass(self, username, password):
        """
        检查用户名和密码是否已输入，若无则手动输入
        """
        if username is None:
            username = self.login_data.get("username")
            if not username:
                username = input("请输入手机号：")
        if "+86" not in username:
            username = "+86" + username

        if password is None:
            password = self.login_data.get("password")
            if not password:
                password = input("请输入密码：")
        return username, password

    def download(self, url):
        res = self.session.get(url, headers=self.session.headers)
        if res.status_code // 100 != 2 and res.status_code // 100 != 3:
            logger.error("request failed, status {}".format(res.status_code))
        return res.text or None
