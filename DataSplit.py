import pandas as pd

path = r'.\消防数据\扩展版数据.xlsx'
df = pd.read_excel(path)

# 划分成火灾、救援和救助
df_fire = df[df['案件类型']=='火灾']
df_resc = df[df['案件类型']=='抢险救援']
df_asst = df[df['案件类型']=='社会救助']

df_fire.to_csv('./消防数据/数据切分/fire.csv')
df_resc.to_csv('./消防数据/数据切分/rescue.csv')
df_asst.to_csv('./消防数据/数据切分/assist.csv')

def hierarchi_save(df_fire, name):
    # 火灾分级
    fire_0 = df_fire[df_fire['案件等级']=='零级']
    if len(fire_0) > 0:
        fire_0.to_csv('./消防数据/数据切分/' + name + '_0.csv')
    fire_1 = df_fire[df_fire['案件等级']=='一级']
    if len(fire_1) > 0:
        fire_1.to_csv('./消防数据/数据切分/' + name + '_1.csv')
    fire_2 = df_fire[df_fire['案件等级']=='二级']
    if len(fire_2) > 0:
        fire_2.to_csv('./消防数据/数据切分/' + name + '_2.csv')
    fire_3 = df_fire[df_fire['案件等级']=='三级']
    if len(fire_3) > 0:
        fire_3.to_csv('./消防数据/数据切分/' + name + '_3.csv')
    fire_4 = df_fire[df_fire['案件等级']=='四级']
    if len(fire_4) > 0:
        fire_4.to_csv('./消防数据/数据切分/' + name + '_4.csv')
    fire_5 = df_fire[df_fire['案件等级']=='五级']
    if len(fire_5) > 0:
        fire_5.to_csv('./消防数据/数据切分/' + name + '_5.csv')

hierarchi_save(df_fire, 'fire')
hierarchi_save(df_resc, 'rescue')
hierarchi_save(df_asst, 'assist')



# heat_data = [[row['GIS_Y'], row['GIS_X']] for index, row in df_data.iterrows()]
# heat_data = np.array(heat_data)