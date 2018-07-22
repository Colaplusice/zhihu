import csv
import jieba
from gensim.models import word2vec
import re
import numpy as np
import random

class Means:

    def __init__(self):
        self.model=word2vec.Word2Vec.load('NLP/jieba.model')

    #提取和处理信息
    def get_message_from_csv(self):
        r=re.compile('[’!"，。！#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]+')
        word_list=[]
        with open('message.csv','r') as opener:
            headLine_message=[]
            reader=csv.reader(opener)
            for i in reader:
                if i[2]:
                    each = r.sub('', i[2])
                    cut_res=jieba.cut(each,cut_all=False,HMM=False)
                    for each in cut_res:
                        if len(each)>1 and not all(ord(c)<128 for c in each):
                            word_list.append(each)
                            break
                    cut_result = ' '.join(cut_res)
                    headLine_message.append(cut_result)
                elif i[7]:
                    each = r.sub('', i[7])
                    cut_result = ' '.join(jieba.cut(each, cut_all=False, HMM=False))
                    headLine_message.append(cut_result)
        return (headLine_message[1:],word_list[1:])

    #写入csv
    def write_to_txt(self):
        list=self.get_message_from_csv()
        with open('NLP/jieba.txt','w') as opener:
            for each in list:
                opener.writelines(each)
        print('分词完成')

    def k_means(self):
        word_lis=self.get_message_from_csv()[1]
        vector_list=[]
        error=0
        for each in word_lis:
            print(each)
            try:
                vector_list.append(self.model[each])
            except:
                continue
        self.Means(3,vector_list)

    def Means(self,k, dataset):
        data = np.array(dataset)
        n = len(data)
        print(n)
        s = 0
        # 所有的中心点
        centers = []
        # 每一个中心点
        Num = []
        # 初始化 centers 代表中心的集合  center代表中心里的点的集合
        for i in range(k):
            center = []
            sd = random.randint(0, n - 1)
            Num.append(sd)
            center.append(dataset[sd])
            centers.append(center)
            # 计算每个点的归属，添加的对应的中心集合中
            # 计算虚拟的中心然后传入 calcenter中
            visualcenter = []
            testNUm = []
        while (1):
            num = []
            for i in range(k):
                nu = []
                num.append(nu)
            visualcenter = []
            for each in centers:
                each = np.array(each)
                each = each.astype('float64')
                value = sum(each)
                value = value / len(each)
                visualcenter.append(value)
            for i in range(n):
                which = self.CalDis(visualcenter, dataset[i])
                num[which].append(i)
                # print("this is which:"+str(which))
                centers[which].append(dataset[i])
            num = np.array(num)
            if (len(testNUm) == 0):
                # print(testNUm)
                # print(num)
                testNUm = num
                s += 1
                print("第" + str(s) + "次迭代")
            elif (testNUm == num).all():
                print("分类不会变化了")
                for each in visualcenter:
                    print(each)
                print(num)
                return num
            else:
                # print(testNUm)
                # print(num)
                testNUm = num
                s += 1
                print("第" + str(s) + "次迭代")

    # 计算出距离最小的中心点 两个参数 center是k个中心点的list,vectora是要求的点
    def CalDis(self,centers, vectora):
        # print("this is center:"+str(centers))
        k = len(centers)
        result = []
        # print("this is k"+str(k))
        for i in range(k):
            centera = np.array(centers[i])
            vectora = np.array(vectora)
            centera = centera.astype('float64')
            vectora = vectora.astype('float64')
            res = np.square(centera - vectora)
            res = sum(res)
            res = np.sqrt(res)
            result.append(res)
        index = 0
        Max = 10000
        for i in range(len(result)):
            if result[i] < Max:
                Max = result[i]
                index = i
        return index

    # message_list=get_message_from_csv()

    #训练模型
    def train_model(self):
        sentences=word2vec.Text8Corpus('NLP/jieba.txt')
        model=word2vec.Word2Vec(sentences,min_count=1,workers=2,hs=1,negative=0)
        model.save('NLP/jieba.model')
        print(model['你'])
        y1=model.similarity('你','你们')
        print(y1)


    def get_keys(self):
        keys=self.model.wv.vocab.keys()


        pass
    def cal_distance(self,word_1,word_2):
        return self.model.similarity(word_1,word_2)

means=Means()
# means.get_message_from_csv()

means.k_means()
# means.train_model()
#
# print(result[1])
# print(type(result[1]))
# print(result[2])

# means.train_model()
# write_to_txt()
# load_model()
