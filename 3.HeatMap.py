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

def heat_map_plot(df_data, name):
    # 获取所需数据
    heat_data = [[row['GIS_Y'], row['GIS_X']] for index, row in df_data.iterrows()]
    heat_data = np.array(heat_data)
    # 删除包含nan的行
    heat_del_nan = heat_data[~np.isnan(heat_data).any(axis=1)]

    # 高德地图
    #tiles='https://wprd01.is.autonavi.com/appmaptile?x={x}&y={y}&z={z}&lang=zh_cn&size=1&scl=1&style=7'
    shanghai = folium.Map(location=[31.1468, 121.4979],
                   zoom_start=10,
                   tiles='http://thematic.geoq.cn/arcgis/rest/services/StreetThematicMaps/Gray_OnlySymbol/MapServer/tile/{z}/{y}/{x}',
                   attr='街道网图',
                   )
    # 添加热力图层
    # gradient = {0.2: 'blue', 0.4: 'green', 0.6: 'yellow', 1: 'red'}
    HeatMap(heat_del_nan, name='热力图',  min_opacity=0.2).add_to(shanghai)

    # 绘制行政边界
    f = open('./地图数据/乡镇边界/上海市_乡镇边界.json', encoding='utf-8')
    content = f.read()
    geo_json = json.loads(content)
    # 将边界数据添加到地图上
    folium.GeoJson(data=geo_json).add_to(shanghai)

    # # 绘制消防站点位置
    # path = './数据/消防站情况.xlsx'
    # data = pd.read_excel(path)
    # station_pos = [[row['纬度'], row['经度']] for index, row in data.iterrows()]
    #
    # # 创建圆形，设置圆心、半径和填充颜色
    # for si in station_pos:
    #     folium.Circle(
    #         location=si,
    #         radius=50,  # 半径以米为单位
    #         popup='圆形',
    #         color='black',
    #         fill=False,
    #     ).add_to(shanghai)

    # shanghai.fit_bounds([[120.52, 30.40],
    #                [122.12, 30.40],
    #                [120.53,31.53],
    #                [122.12, 31.53]])  # 根据范围缩放地图

    root = shanghai.get_root()
    html = root.render()  # 这个拿到的就是一个html的内容
    # mo.save('text.html')
    # 2.使用Html2Image将地图html文件转成png
    base = Path(__file__).resolve().parent
    # 以下为Html2Image参数的2中写法，custom_flags参数是网页生成后延迟10秒生成图片（地图加载慢，眼部就会出现空白方块，output_path 是文件生成后存储的文件夹，screenshot为生成图片的方法）
    hti = Html2Image(custom_flags=['--virtual-time-budget=3000', '--hide-scrollbars'])
    hti.output_path = os.path.join(base, 'map_png')
    save_name = name + '.png'
    print(save_name)
    hti.screenshot(html_str=str(html), save_as=save_name)

    #
    # 保存地图为html
    save_name = '.\结果输出\\' + name + '.html'
    print('正在保存' + save_name)
    shanghai.save(save_name)

name_list = ['零级', '一级', '二级', '三级', '四级', '五级']
for name in name_list:
    df_data = df.loc[df['案件等级'] == name]
    heat_map_plot(df_data, name)

