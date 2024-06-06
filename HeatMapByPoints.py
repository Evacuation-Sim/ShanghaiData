import numpy as np
from scipy import stats
import pandas as pd

# 生成一组用于绘制估计概率密度函数的点
path = r'.\消防数据\数据切分\零级数据.csv'
df_data = pd.read_csv(path)
# df_data = df_data[df_data[]]

heat_data = [[row['GIS_Y'], row['GIS_X']] for index, row in df_data.iterrows()]
heat_data = np.array(heat_data)
# 删除包含nan的行
heat_data = heat_data[~np.isnan(heat_data).any(axis=1)]
# 使用 stats.gaussian_kde 进行核密度估计
kde = stats.gaussian_kde(heat_data.T)
print(heat_data.T)

x = np.linspace(min(heat_data.T[0]), max(heat_data.T[0]), 200)
y = np.linspace(min(heat_data.T[1]), max(heat_data.T[1]), 200)
X, Y = np.meshgrid(x, y)
positions = np.vstack([X.ravel(), Y.ravel()])
Z = np.reshape(kde(positions).T, X.shape)

# 绘制估计的概率密度函数
import matplotlib.pyplot as plt
plt.contourf(X, Y, Z, cmap='Reds')
plt.xlabel('X1')
plt.ylabel('X2')
plt.title('Kernel Density')
plt.colorbar()
plt.show()

