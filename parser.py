import csv
import json

from bs4 import BeautifulSoup

from logs import logger


class Parser:
    def __init__(self):
        pass

    def parse2dict(self, html):
        raise NotImplementedError


class ZhihuParser(Parser):
    def parse2dict(self, current_user, html):
        if not html:
            return {}
        """
        xpath
        //script/[@id="js-initialData"]
        """
        # 数据清洗
        soup = BeautifulSoup(html, "html.parser")
        html_data = soup.find("script", {"id": "js-initialData"})
        if html_data is None:
            logger.warning("html data is None!")
            return {}
        json_data = json.loads(html_data.text)
        users = json_data["initialState"]["entities"]["users"]
        users.pop(current_user, None)
        return users

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
