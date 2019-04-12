# 知乎爬虫框架实践&数据科学实战

## intro

爬虫架构实践: 从登录下载到解析数据，构建模型保存数据，到数据清洗和分析。对各个功能模块解耦合。
通过对个人信息的抓取，和用户信息的分析，完成了用户图网络的构建

大致思路： 从用户S开始，抓取用户following的信息，再通过dfs来将user_following的following加入爬虫队列，
构建用户信息的图网络结构

ps: 破解登录参考: [awesome-python-login-model](https://github.com/CriseLYJ/awesome-python-login-model)

## 架构设计

一个爬虫需要做的事情:
1. downloader: 登录验证，维护cookie，破解反爬虫，成功获取到html消息
3. extract解析信息 将有用的数据从网页中抽取出来,将数据转换为不同的格式,json,dict,list
4. save保存数据,保存视频，保存数据到csv, 到database...

- downloader.py  负责登录，抓取模块
- Throttle.py 防止爬虫被禁止，每个页面抓取的时候，采取一定的延迟时间
- parser.py  负责解析html信息
- saver.py   对抓取的数据进行保存  

main.py

爬虫的主线程：
维持一个url队列，当已经抓取的url大于1000时或者队列为空时爬虫停止
否则从队列中pop出一个未抓取过的url然后进行抓取


这些功能块应该解耦合，相互之间不应该有依赖。并且具有一定的普适性，传入不同的解析标准，
传入不同的url，应该是通用的。

## 登录

加载cookies，检查是否登录，cookies是否过期，如果已登录，则返回True，否则进行登录
首先加载cookie,然后更新两个参数:
 xsrf:防止跨站请求
authorization:授权登录的码，是固定的
然后检查用户名密码是否输入，如果没有则在终端输入
然后更新data的值,更新的内容有:
captcha:验证码请求，无论是否需要都要请求一次，如果需要验证码，则手动输入
timestamp:请求的时间戳，为11位
signiture:根据时间戳计算的签名

发起post请求
如果成功则返回true,否则抛出异常


### update login  2019.4.10 

更新登录的请求:
1. headers中加入     
'content-type': 'application/x-www-form-urlencoded',  
'accept-encoding': 'gzip, deflate, br',

2. 根据encrypt.js 对Post数据进行加密
3. 对post验证码方法进行更新

## 抓取数据

登录的信息保存在request的session会话中，
登录个人的关注者界面，抓取html,然后进行解析
从html中，将json值抓取下来
知乎把个人信息全藏在 data-state域中，通过 传递json数据到主页
然后主页再通过动态加载，将数据填入相应的table
抓取这个用户关注的用户
再通过抓取这个用户关注的用户的用户
然后进行数据清洗
将json值存在数据库中，进行用户信息的保存

## 数据模型

- headline 简介
- name:姓名
- gender:性别 0为女性
- answerCount:答案
- followerCount:关注者

## 数据处理

1. 对每个用户的headline进行标签
2. 缺失值处理，对于没有headline的用户，不进行处理
3. 采用jieba进行分词
4. 想要根据词条来对用户进行聚类。k-means聚类算法，采用word2vec 计算词条之间的相似度，然后采用k-means算法进行聚类

## todo

1. handle_data中的k_means聚类重写
2. 数据可视化方面完成

## debug&mention

- 知乎的信息可以直接从网页中的json获得
- 在递归添加url时，要注意对添加过的点进行排除，也就是dfs中灰色的点，因为这个图网络可以一直递归到所有用户，所以只能通过手动设置上限来终止，
所以没有黑色的点。








