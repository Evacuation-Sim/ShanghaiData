# 统计不同火灾等级的平均出警时间
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
from scipy.stats import poisson

config = {
    "font.family": 'serif',
    "font.size": 14,
    "mathtext.fontset": 'stix',
    "font.serif": ['SimSun'],
}
rcParams.update(config)

path = r'.\消防数据\出警时长.xlsx'
df = pd.read_excel(path)



# 筛选火灾数据
df = df[df['案件类型'] == '火灾']
print("火灾报警总数：", len(df))
# 筛选实警
df = df[df['案件性质'] == '实警']
print("火灾实警总数：", len(df))

cnum_list = []
time_list = []
class_list = ['零级', '一级', '二级', '三级', '四级', '五级']

for class_i in class_list:
    df_i = df[df['案件等级']==class_i]
    time_i = df_i['案件总现场时长']
    cnum_i = len(df_i['案件总现场时长'])
    time_i.dropna()
    time_list.append(np.mean(time_i))
    cnum_list.append(cnum_i)

fig = plt.figure(figsize=(14, 6))
ax1 = fig.add_subplot(121)
index_x = ['0', '1', '2', '3', '4', '5']
ax1.bar(index_x, cnum_list, width=0.5)
# 在每个柱子上方添加数值
for i, v in enumerate(cnum_list):
    plt.text(i, v+100, v, ha='center', va='bottom')
ax1.set_ylim([0, 10000])
ax1.set_yticklabels(['0k', '2k', '4k', '6k', '8k', '10k'])
ax1.set_xlabel('Case Level')
ax1.set_ylabel('Case Number')
plt.title('(a)')


ax2 = ax1.twinx()
x2 = [0, 1, 2, 3, 4, 5]
y2 = poisson.pmf(x2, 0.994)

ax2.plot(x2, y2, marker='D', linestyle='-',
    color='red',
    label='Fit result')
ax2.set_ylim([0, 10000/np.sum(cnum_list)])
ax2.set_ylabel('frequency')

plt.legend()


ax3 = fig.add_subplot(122)
ax3.bar(index_x, time_list, width=0.5)
# 在每个柱子上方添加数值
for i, v in enumerate(time_list):
    plt.text(i, v+100, round(v), ha='center', va='bottom')

x3 = np.array([0, 1, 2, 3, 4, 5])
a, b = 3.27213977, 2.03137632
y3 = a*np.exp(b*x3)

ax3.plot(x3, y3, marker='D', linestyle='-',
    color='red',
    label='Fit result')
ax3.set_yticklabels(['0k', '10k', '20k', '30k', '40k', '5k', '60k', '70k', '80k'])
ax3.set_xlabel('Case Level')
ax3.set_ylabel('Mean Time(min)')
plt.title('(b)')
plt.legend()

plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, wspace=0.3)
plt.savefig("./结果输出/freq_time.pdf", dpi=300, format="pdf")

df_res = pd.DataFrame()
df_res['level'] = index_x
df_res['freq'] = cnum_list
df_res['time'] = time_list
df_res.to_csv('./结果输出/freq_time.csv')
plt.show()





