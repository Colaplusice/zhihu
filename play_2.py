import requests
from Config import headers

session = requests.session()

response = session.post(url="https://www.zhihu.com/signup?next=%2F", headers=headers)


print(response.cookies)
