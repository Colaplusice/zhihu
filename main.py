__author__ = "Colaplusice"
__github__ = "https://github.com/Colaplusice/zhihu"

from crawler_utils import MongoCache

from throttle import Throttle

# need to customize
from configs import BEGIN_URL, PHONE_NUMBER, PASSWORD
from downloader import ZhihuDownloader
from logs import logger
from parser import ZhihuParser
from saver import ZhihuSaver


class Crawler:
    def __init__(
        self, cache, downloader, parser, begin_url=BEGIN_URL, throttle=None, saver=None
    ):
        self.downloader = downloader
        self.downloader.login(username=PHONE_NUMBER, password=PASSWORD)
        self.dict = {}
        self.cache = cache
        self.begin_url = begin_url
        # self.delay = 5
        self.throttle = throttle
        self.user_url = "https://www.zhihu.com/people/{}/following"
        self.parser = parser
        self.saver = saver if saver is not None else cache

    def run(self):
        """
        DFS add  user into queue
          found user add user's followed into queue
        """

        def add_user_in_queue(user_dict):
            if len(url_queue) >= 1000 - finished:
                logger.info("url queue fulled")
                return
            for user in user_dict.keys():
                # 将新用户主页抓取 添加到url_queue中
                user_data = self.cache[user]
                if user_data is None:
                    url_queue.append(self.user_url.format(user))
                #  color black, means visited
                elif user_data.get("color") != "black":
                    self.cache.collection.update_one(
                        {"_id": user}, {"$set": {"color": "black"}}, upsert=False
                    )
                    add_user_in_queue(user_data)

        finished = len(self.cache)
        url_queue = [self.begin_url]
        while url_queue and finished < 1000:
            url = url_queue.pop()
            current_user = url.split("/")[-2]
            # user info has crawled
            user_dict = self.cache[current_user]
            if user_dict:
                logger.info("user :{} exists in cache".format(current_user))
            else:
                finished += 1
                # download and parse html
                logger.info("url出队列:{}".format(url))
                logger.info("第{}个页面".format(finished))
                html = self.cache[url].get("html") if self.cache[url] else None
                if html is None:
                    html = self.downloader.download(url)
                    self.cache.collection.update_one(
                        {"_id": url}, {"$set": {"html": html}}, upsert=True
                    )
                    self.throttle.wait(url)
                else:
                    print("load user html from cache {}".format(current_user))
                user_dict = self.parser.parse2dict(current_user, html)
                self.cache[current_user] = user_dict
            if len(url_queue) < 1000 - finished:
                add_user_in_queue(user_dict)


if __name__ == "__main__":
    downloader = ZhihuDownloader()
    # phone_number = "your phone"
    # password = "your pass"
    mongo_cache = MongoCache(db_name="zhihu", collection_name="default")
    parser = ZhihuParser()
    saver = ZhihuSaver
    begin = Crawler(
        cache=mongo_cache,
        downloader=downloader,
        parser=parser,
        begin_url=BEGIN_URL,
        throttle=Throttle(delay=1),
    )
    begin.run()
