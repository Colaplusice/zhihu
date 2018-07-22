import csv
import pandas as pd
import numpy as np
import xlrd,openpyxl
from pandas import Series,DataFrame
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']


def csv2xlxs():
    csv=pd.read_csv('message.csv',encoding='utf-8')
    csv.to_excel('message.xlsx',sheet_name='data')

csv=pd.read_csv('message.csv',encoding='utf-8')
csv.hist()
plt.show()
csv.plot(kind='density', subplots=True, layout=(3,3), sharex=False,fontsize=8,figsize=(8,6))
plt.show()

correlations=csv.corr()
fig=plt.figure()


ax = fig.add_subplot(111)
cax = ax.matshow(correlations, vmin=-1, vmax=1)  #绘制热力图，从-1到1
fig.colorbar(cax)  #将matshow生成热力图设置为颜色渐变条
ticks = np.arange(0,9,1) #生成0-9，步长为1
ax.set_xticks(ticks)  #生成刻度
ax.set_yticks(ticks)
names=['url,昵称,标题,性别,回答数目,关注者,文章,描述']
ax.set_xticklabels(names) #生成x轴标签
ax.set_yticklabels(names)
plt.show()