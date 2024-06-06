# 确定每个点的AOI属性
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

df_pt = pd.read_csv('./结果输出/points.csv', encoding='gbk')

shapefile = r'.\地图数据\上海市_AOI面.shp'
shp_file = gpd.read_file(shapefile)
print(len(shp_file))

type1_list = []
type2_list = []
type3_list = []
stru_list = []
for index, row in df_pt.iterrows():
    point = Point(row[0], row[1])
    flag = False
    for index, row in shp_file.iterrows():
        if row.geometry.contains(point):
            type1_list.append(row['type1'])
            type2_list.append(row['type2'])
            type3_list.append(row['type3'])
            stru_list.append(row['结构'])
            flag = True
            print('YES')
            break
    if not flag:
        type1_list.append('Nan')
        type2_list.append('Nan')
        type3_list.append('Nan')
        stru_list.append('Nan')
df_pt['type1'] = type1_list
df_pt['type2'] = type2_list
df_pt['type3'] = type3_list
df_pt['结构'] = stru_list

df_pt.to_csv('./结果输出/points_add.csv', encoding='gbk')


