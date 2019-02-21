import requests, time
from bs4 import BeautifulSoup
import urllib2, urllib
import cookielib
from Config import headers, email, phone_number, password

url = "https://www.zhihu.com/login/email"


def get_captcha(data):
    with open("captcha.gif", "wb") as fb:
        fb.write(data)
    return input("captcha")


class ZhiHu:
    def __init__(self):
        self.headers = headers
        self.email = email
        self.password = password
        self.phone_number = phone_number

    def get_xsrf(self):
        begin_url = "https://www.zhihu.com/#signin"
        # sessina=requests.session()
        req = requests.get(url, headers=headers)

        print(req.text)
        html_content = req.text
        print(req.status_code)

        soup = BeautifulSoup(html_content, "html.parser")

        _xsrf = soup.find("input", attrs={"name": "_xsrf"}).get("value")
        print(_xsrf)

    def login_in(self):

        session = requests.session()
        _xsrf = "fa21689-2ffa-f4b55-b39b-942c6ab89824"
        data = {
            "username": self.phone_number,
            "password": self.password,
            "_xsrf": _xsrf,
        }
        login_page = session.post(
            data=data, url="https://www.zhihu.com/signin", headers=self.headers
        )
        login_code = login_page.text
        print(login_page.status_code)

        print(login_code)

    def login_lib(self):
        begin_url = "https://www.zhihu.com/signin"

        _xsrf = "fa21689-2ffa-f4b55-b39b-942c6ab89824"

        data = {"phone_num": self.phone_number, "password": self.password}
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        encode_data = urllib.urlencode(data)
        request = urllib2.Request(url=begin_url, headers=headers, data=encode_data)
        response = opener.open(request)
        print(response.geturl())
        print(response.read())


# def login(username, password, oncaptcha):
#
#     _xsrf = BeautifulSoup( 'html.parser').find(
#         'input', attrs={'name': '_xsrf'}).get('value')
#
#     captcha_content = sessiona.get('https://www.zhihu.com/captcha.gif?r=%d&type=login' % (time.time() * 1000),
#                                    headers=headers).content
#     data = {
#         "_xsrf": _xsrf,
#         "email": username,
#         "password": password,
#         "remember_me": True,
#         "captcha": oncaptcha(captcha_content)
#     }
#     resp = sessiona.post('https://www.zhihu.com/login/email', data, headers=headers).content
#     print(resp)
#     return resp


if __name__ == "__main__":
    # login('18340071291', 'f12580f', get_captcha)
    zhihu = ZhiHu()
    # zhihu.get_xsrf()
    # zhihu.login_in()
    zhihu.login_lib()
