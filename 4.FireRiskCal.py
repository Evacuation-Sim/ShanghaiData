import folium
import pandas as pd
import numpy as np
from folium.plugins import HeatMap
import json
from pathlib import Path
from html2image import Html2Image
import os

path = r'.\消防数据\扩展版数据.xlsx'
df = pd.read_excel(path)
df = df[df['案件类型'] == '火灾']
# 筛选实警
df = df[df['案件性质'] == '实警']

# data = pd.read_excel(path)
import numpy as np
from scipy import stats
import pandas as pd
import geopandas as gpd

def heat_map_init(path):
    # 生成一组用于绘制估计概率密度函数的点

    df_data = pd.read_csv(path)
    # df_data = df_data[df_data[]]

    heat_data = [[row['GIS_Y'], row['GIS_X']] for index, row in df_data.iterrows()]
    heat_data = np.array(heat_data)
    # 删除包含nan的行
    heat_data = heat_data[~np.isnan(heat_data).any(axis=1)]
    # 使用 stats.gaussian_kde 进行核密度估计
    kde = stats.gaussian_kde(heat_data.T)

    return kde

# 读取aoi数据
shapefile = r'.\地图数据\上海市_AOI面.shp'
shp_file = gpd.read_file(shapefile)

path = r'.\消防数据\数据切分\fire.csv'
kde_fire = heat_map_init(path)
path = r'.\消防数据\数据切分\rescue.csv'
kde_resc = heat_map_init(path)
path = r'.\消防数据\数据切分\assist.csv'
kde_asst = heat_map_init(path)

df_data = pd.DataFrame()
GIS_X = []
GIS_Y = []
FireRisk = []
AsstRisk = []
RescRisk = []


index_all = len(shp_file)
for index, row in shp_file.iterrows():
    print(index, index_all)
    x, y = row['wgs_lat'], row['wgs_lng']
    GIS_X.append(x)
    GIS_Y.append(y)
    kde_res = kde_fire([x, y])[0]
    FireRisk.append(kde_res)
    kde_res = kde_resc([x, y])[0]
    RescRisk.append(kde_res)
    kde_res = kde_asst([x, y])[0]
    AsstRisk.append(kde_res)

df_data['GIS_X'] = GIS_X
df_data['GIS_Y'] = GIS_Y
df_data['FireRisk'] = FireRisk
df_data['RescRisk'] = RescRisk
df_data['AsstRisk'] = AsstRisk

df_data.to_csv('./结果输出/RiskData.csv')





