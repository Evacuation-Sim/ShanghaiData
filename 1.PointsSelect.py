import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False

shapefile = r'.\地图数据\上海市_县界.shp'
shp_file = gpd.read_file(shapefile)
print(shp_file.head())

# shp_file.plot()
# plt.show()


from shapely.geometry import Point

# 创建点对象
point = Point(121.917041, 31.006204)
# 判断点是否在每个区域内
idx_list = []
for index, row in shp_file.iterrows():
    idx_list.append(index)
    if row.geometry.contains(point):
        print("该站点在区域：", index)

shp_file['level'] = idx_list
name_list = ['崇明', '奉贤', '虹口', '徐汇', '嘉定', '金山', '静安', '闵行', '浦东', '青浦', '松江', '徐汇', '杨浦', '长宁', '普陀', '宝山']
shp_file['name'] = name_list

ax = shp_file.plot(
    column="level",
    scheme="BoxPlot",
    edgecolor='k',
    cmap="OrRd",  # 设置分层设色标准
    legend=True,
    # 通过interval设置是否展示区间间隔
    legend_kwds={"loc": "center left", "bbox_to_anchor": (1, 0.5), "interval": True}
)

# # 显示各地级市包含区县数量
# for index in shp_file.index:
#     x = shp_file.iloc[index].geometry.centroid.x
#     y = shp_file.iloc[index].geometry.centroid.y
#     name = shp_file.iloc[index]["name"]
#     ax.text(x, y, name, ha="center", va="center", color='white')

X = np.linspace(120, 122, 50)  # 经向100个点
Y = np.linspace(30, 32, 50)  # 纬向100个点
pt_list = []

for x in X:
    for y in Y:
        point = Point(x, y)
        for index, row in shp_file.iterrows():
            if row.geometry.contains(point):
                if index != 0:
                    pt_list.append([x, y, index])

X = []
Y = []
P = []
for pt in pt_list:
    plt.scatter(pt[0], pt[1], s=2, c='g')
    X.append(pt[0])
    Y.append(pt[1])
    P.append(name_list[pt[2]])

df = pd.DataFrame()
df['GIS_X'] = X
df['GIS_Y'] = Y
df['行政区'] = P

df.to_csv('./结果输出/points.csv', encoding='gbk', index=False)

# for pt in pt_list:
#     plt.scatter(pt[0], pt[1], s=2, c='g')
# plt.show()
