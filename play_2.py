from pymongo import MongoClient
import csv
import datetime
client=MongoClient('localhost',27017)
db=client.zhihu
table=db.message

def get_message_from_db():
    client = MongoClient('localhost', 27017)
    db = client.zhihu
    table = db.message
    list=[item for item in table.find()]
    return list


# dicts={'_id': 'https://www.zhihu.com/people/bu-ding/following', 'result': {'昵称': '布丁', '标题': None, '性别': '男', '回答数目': 90, '关注者': 7012, '文章': 4, '描述': None}, 'timestamp': datetime.datetime(2018, 6, 4, 3, 58, 17, 771000)},
#
# print(list(dicts.keys()))


def write_to_csv(lists):
    index = ['url','昵称','标题', '性别', '回答数目', '关注者', '文章', '描述']
    with open('message.csv','w') as opener:
        writer = csv.writer(opener)
        writer.writerow(index)
        for (ind,each) in enumerate(lists):
            result_dict=each.get('result')
            url=each.get('_id')
            sd=[url]
            sd.extend(list(result_dict.values()))
            writer.writerow(sd)

lists=get_message_from_db()
write_to_csv(lists)



