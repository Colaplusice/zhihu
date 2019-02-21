__author__ = "IceCola"
__zhihu__ = ""
__github__ = ""
import requests
from bs4 import BeautifulSoup
import time
import re
import base64
import hmac
import hashlib
import json
import matplotlib.pyplot as plt
from http import cookiejar
from PIL import Image
import lxml.html
import csv
from Config import *
from MongoCache import Mongo_cache, Mongo_html_cache
from Throttle import Throttle


class ZhihuAccount(object):
    def __init__(self):
        self.login_url = LOGIN_URL
        self.login_api = LOGIN_API
        self.login_data = FORM_DATA.copy()
        self.session = requests.session()
        self.session.headers = HEADERS.copy()
        self.session.cookies = cookiejar.LWPCookieJar(filename="./cookies.txt")
        self.begin_url = begin_url

    #
    # def get_url(self):
    #     req=self.session.get(self.begin_url)
    #     html=req.text
    #     soup = BeautifulSoup(html, 'html.parser')
    #     page_content = soup.find_all('a',{"class":"Button GlobalSideBar-navLink Button--plain"})
    #     for each in page_content:
    #         print(each)
    #
    #     with open('zhihu_html.text','w') as opener:
    #         opener.write(html)

    def get_content(self):
        html = ""
        with open("zhihu_html.text", "r") as opener:
            html = opener.read()

        json_html = json.loads(html)
        json_data = json_html["data"]
        print(json_data)

        # soup = BeautifulSoup(html, 'html.parser')
        # page_content = soup.find_all('a', {"class": "Button GlobalSideBar-navLink Button--plain"})
        # for each in page_content:
        #     print(each)
        #     print('*'*50)

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
                return True

        headers = self.session.headers.copy()
        headers.update(
            {
                "authorization": "oauth c3cef7c66a1843f8b3a9e6a1e3160e20",
                "X-Xsrftoken": self._get_token(),
            }
        )
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

        resp = self.session.post(self.login_api, data=self.login_data, headers=headers)
        if "error" in resp.text:
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
        except FileNotFoundError:
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
        print(resp.headers)
        print(resp.status_code)
        token = re.findall(r"_xsrf=([\w|-]+)", resp.headers.get("Set-Cookie"))[0]
        return token

    def _get_captcha(self, headers):
        """
        请求验证码的 API 接口，无论是否需要验证码都需要请求一次
        如果需要验证码会返回图片的 base64 编码
        根据头部 lang 字段匹配验证码，需要人工输入
        :param headers: 带授权信息的请求头部
        :return: 验证码的 POST 参数
        """
        lang = headers.get("lang", "en")
        if lang == "cn":
            api = "https://www.zhihu.com/api/v3/oauth/captcha?lang=cn"
        else:
            api = "https://www.zhihu.com/api/v3/oauth/captcha?lang=en"
        resp = self.session.get(api, headers=headers)
        show_captcha = re.search(r"true", resp.text)
        if show_captcha:
            put_resp = self.session.put(api, headers=headers)
            img_base64 = re.findall(r'"img_base64":"(.+)"', put_resp.text, re.S)[
                0
            ].replace(r"\n", "")
            with open("./captcha.jpg", "wb") as f:
                f.write(base64.b64decode(img_base64))
            img = Image.open("./captcha.jpg")
            if lang == "cn":
                plt.imshow(img)
                print("点击所有倒立的汉字，按回车提交")
                points = plt.ginput(7)
                capt = json.dumps(
                    {
                        "img_size": [200, 44],
                        "input_points": [[i[0] / 2, i[1] / 2] for i in points],
                    }
                )
            else:
                img.show()
                capt = input("请输入图片里的验证码：")
            # 这里必须先把参数 POST 验证码接口
            self.session.post(api, data={"input_text": capt}, headers=headers)
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

    def load_local_following_html(self):
        try:
            with open("following.txt", "r") as opener:
                html = opener.read()
        except FileNotFoundError:
            print("file not found, begin download")
            url = "https://www.zhihu.com/people/fan-jia-liang-57/following"
            resp = self.session.get(url)
            print(resp.status_code)
            html = resp.text
            with open("following.txt", "w") as opener:
                opener.write(html)
        return html

    def download(self, url):
        # if not self.check_login():
        #     print('未登录，开始登陆')
        #     print(username,password)
        #     self.login(username=username,password=password)
        response = self.session.get(url)
        if response.text:
            print("页面下载完成")
            return response.text
        else:
            raise FileNotFoundError("html为空")

    def url_formate(self, username):
        base_url = "https://www.zhihu.com/people/{}/following"
        url = base_url.format(username)
        return url

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


class Beginer:
    def __init__(
        self,
        Mongo_cache=None,
        downloader=ZhihuAccount(),
        begin_url="https://www.zhihu.com/people/fan-jia-liang-57/following",
        throttle=None,
        html_mon_cache=None,
    ):
        self.downloader = downloader
        self.dict = {}
        self.Mongo_cache = Mongo_cache
        self.html_mon_cache = html_mon_cache
        self.begin_url = begin_url
        # self.delay = 5
        self.throttle = throttle

    # 提取html中的message 返回dict类型
    def parse_html(self, html):
        # 数据清洗
        soup = BeautifulSoup(html, "html.parser")
        state_datas = soup.find("div", {"id": "data"})
        state_data = state_datas["data-state"]
        json_data = json.loads(str(state_data))
        users = json_data["entities"]["users"]
        dicts = {}
        # try:
        for (k, v) in users.items():
            # print(k,v)
            try:
                if k != "fan-jia-liang-57":
                    values = {
                        "昵称": v["name"],
                        "标题": v["headline"]
                        if not re.findall("<a.*?/a>", v["headline"])
                        else "",
                        "性别": "女" if v["gender"] == 0 else "男",
                        "回答数目": v["answerCount"] if v.get("answerCount") else "",
                        "关注者": v["followerCount"],
                        "文章": v["articlesCount"],
                        "描述": v["description"] if v.get("description") else "",
                    }
                    url = self.url_formate(k)
                    dicts[url] = values
                    if not dicts:
                        print(dicts)
                        raise FileNotFoundError("html内容错误，无法获得用户信息")
            except KeyError:
                print("出错了..........")
                print(k, v)
                break

        # except (KeyError,FileNotFoundError) as e:
        #     print('数据清洗发送错误')

        return dicts

    # k 代表用户的url,value代表用户的信息，dicts为一页html的所有用户
    def write_to_db(self, dicts):
        for (k, v) in dicts.items():
            try:
                if self.Mongo_cache[k]:
                    print("数据库中已有用户信息")
            except KeyError as e:
                self.Mongo_cache[k] = v
                print("用户信息取缓存失败%s" % e)
                print("写入数据库成功!")

    # 考虑到要去除重复的问题，所以从数据库中读取然后...
    def write_to_csv(self, lists=None):
        lists = self.Mongo_cache.get_all_message()
        index = ["url", "昵称", "标题", "性别", "回答数目", "关注者", "文章", "描述"]
        with open("message.csv", "w") as opener:
            writer = csv.writer(opener)
            writer.writerow(index)
            for (ind, each) in enumerate(lists):
                print(ind)
                result_dict = each.get("result")
                url = each.get("_id")
                sd = [url]
                sd.extend(list(result_dict.values()))
                writer.writerow(sd)

    def url_formate(self, username):
        base_url = "https://www.zhihu.com/people/{}/following"
        url = base_url.format(username)
        return url

    def begin(self):
        self.downloader.login(username=username, password=password)
        n = 1
        url_queue = [self.begin_url]
        seen = {}

        while url_queue and n < 1000:
            url = url_queue.pop()
            print("url出队列:{}".format(url))
            print("第{}个页面".format(n))

            try:
                html = self.html_mon_cache[url]["result"]
                print("从缓存中取得html~")
                dicts = self.parse_html(html)
                # 将url添加在队列中
                for (k, v) in dicts.items():
                    if k not in seen:
                        seen[k] = n
                        n += 1
                        url_queue.append(k)

            except KeyError as e:
                print("取缓存失败，开始下载页面")
                html = self.downloader.download(url)
                self.html_mon_cache[url] = html
                dicts = self.parse_html(html)
                self.throttle.wait(url)
                self.write_to_db(dicts)
                # 将url添加在队列中
                for (k, v) in dicts.items():
                    if k not in seen:
                        seen[k] = n
                        n += 1
                        url_queue.append(k)


if __name__ == "__main__":
    account = ZhihuAccount()
    phone_number = "your phone"
    password = "your pass"
    begin = Beginer(
        Mongo_cache=Mongo_cache(),
        downloader=account,
        begin_url=begin_url,
        throttle=Throttle(delay=5),
        html_mon_cache=Mongo_html_cache(),
    )

    begin.begin()
    # account.login(username=phone_number, password=password, load_cookies=True)
    # account.get_url()

    # account.get_content()
    # account.get_user()
