import jieba
import re
seg_list=jieba.cut("我来到清华大学!",cut_all=False,HMM=False)
sd=','.join(seg_list)
str='我来，到清华大学!'
r = re.compile('[’!"，#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]+')
print(r.sub('',str))


with open('jieba.txt','w') as opener:
    opener.writelines(sd)