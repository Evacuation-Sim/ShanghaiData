# 统计不同火灾等级的平均出警时间
import numpy as np
import pandas as pd
path = r'.\消防数据\出警时长.xlsx'
df = pd.read_excel(path)

df = df[df['案件类型'] == '火灾']

time_list = []
class_list = ['零级', '一级', '二级', '三级', '四级', '五级']

for class_i in class_list:
    df_i = df[df['案件等级']==class_i]
    time_i = df_i['案件总现场时长']
    time_i.dropna()
    time_list.append(np.mean(time_i))
print(time_list)





