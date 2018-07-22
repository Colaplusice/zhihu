知乎爬虫

流程

登录

检查是否登录，如果已登录，则返回True

否则进行登录

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



抓取数据

登录的信息保存在request的session会话中，

登录个人的关注者界面，抓取html,然后进行解析

从html中，将json值抓取下来

知乎把个人信息全藏在 data-state域中，通过 传递json数据到主页

然后主页再通过动态加载，将数据填入相应的table

抓取这个用户关注的用户

再通过抓取这个用户关注的用户的用户

然后进行数据清洗

将json值存在数据库中，进行用户信息的保存



功能模块

ZhihuAccount.py

 负责下载页面

Throttle.py

 防止爬虫被禁止，每个页面抓取的时候，采取一定的延迟时间

MongoCache.py

 将html 和用户message的信息存放在数据库中，如果重复抓取的话先从缓存中读取

如果html信息存在的话，就从数据库中读取

如果用户信息已经存在于数据库中的话，就不进行更新

Beginner.py

爬虫的主线程：

维持一个url队列，当已经抓取的url大于1000时或者队列为空时爬虫停止

否则从队列中pop出一个url然后进行抓取，将抓取到的新url再添加在队列中

如果这个url已经出现过，则不进行添加，防止出现无穷递归



数据结构

将json转换为python的数据结构dict

一个html的dict

{ user1:{},

user2:{},

user3:{},

user4:{}}

一个用户的dict

headline 简介

name:姓名

gender:性别 0为女性

answerCount:答案

followerCount:关注者



遇到的bug

1. 抓取其他用户页面的时候，会显示我的信息，因为我是登录状态来去抓取别人的信息的；但信息中没有我的详细信息，所以在抓取其他页面时应该跳过 当前用户的信息，否则会报KeyError



## 数据处理

1. 对每个用户的headline进行标签
2. 缺失值处理，对于没有headline的用户，不进行处理
3. 采用jie ba进行分词


4. 想要根据词条来对用户进行聚类。k-means聚类算法

采用word2vec 计算词条之间的相似度

然后采用k-means算法进行聚类








