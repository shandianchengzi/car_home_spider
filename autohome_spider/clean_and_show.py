# coding: utf-8
'''
brand,year,model,mileage,registration_time,price,warranty_time,city,link
'''

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import os
file_dir = os.path.dirname(__file__)
os.chdir(file_dir)

# 数据路径和存储结果路径
data_path = 'autohome.csv'
result_path = 'autohome_clean.csv'
imgs_dir = 'imgs'
if not os.path.exists(imgs_dir):
    os.makedirs(imgs_dir)

# 读取数据
df = pd.read_csv(data_path)

# 数据清洗
# 判断清洗结果是否存在
if os.path.exists(result_path):
    df = pd.read_csv(result_path, encoding='gbk') # for windows excel
else:
    df.drop_duplicates(inplace=True) # 去重
    df.dropna(subset=['brand'], inplace=True) # 去掉品牌为空的数据
    # 合并前三列的数据形成字符串，用正则重新解析，查找"xxxx款"，该字符串前面的是brand，后面的是model，中间的是year
    df['brand_model_year'] = df['brand'] + df['year'] + df['model'] # 辅助列
    df['brand'] = df['brand_model_year'].str.extract(r'^(.*?)(\d{4}款)(.*)')[0]
    df['year'] = df['brand_model_year'].str.extract(r'^(.*?)(\d{4}款)(.*)')[1]
    df['model'] = df['brand_model_year'].str.extract(r'^(.*?)(\d{4}款)(.*)')[2]
    df.drop(columns=['brand_model_year'], inplace=True)
    df['year'] = df['year'].replace('款', '', regex=True)
    # 如果原厂保修时间为空，填充为0，否则填充1
    df['warranty_time_exist'] = df['warranty_time'].notnull().astype(int)
    df.to_csv(result_path, index=False, encoding='gbk') # for windows excel

# 数据可视化
df.columns = ['品牌', '上市年份', '车型', '表显里程（公里）', '上牌时间（年）', '价格（万）', '原厂保修时间', '所属城市', '链接']
# 设置字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
# 1. 各种数据的占比统计，全画在一张图上
plt.figure(figsize=(20, 10))
# 1.1 价格分布(只做0~200万的)
plt.subplot(2, 2, 1)
sns.histplot(df['price'], bins=20, kde=True)
plt.xlim(0, 200)
plt.title('价格分布')
# 1.2 里程分布
plt.subplot(2, 2, 2)
sns.histplot(df['mileage'], bins=20, kde=True)
plt.title('里程分布')
# 1.3 品牌分布（前20，扇形图，不要x和y的label）
plt.subplot(2, 2, 3)
df['brand'].value_counts().head(20).plot.pie(autopct='%1.1f%%')
plt.ylabel('')
plt.title('品牌数量分布（前20）')
# 1.4 车型分布(前10，扇形图，不要x和y的label)
plt.subplot(2, 2, 4)
df['model'].value_counts().head(10).plot.pie(autopct='%1.1f%%')
plt.ylabel('')
plt.title('车型数量分布（前10）')
plt.savefig(os.path.join(imgs_dir, '各种数据的占比统计.png'))
# 2 时间分析
plt.figure(figsize=(20, 10))
# 2.1 上牌时间分布
plt.subplot(1, 2, 1)
sns.histplot(df['registration_time'], bins=20, kde=True)
plt.title('上牌时间分布')
# 2.2 上市年份分布
plt.subplot(1, 2, 2)
sns.histplot(df['year'], bins=20, kde=True)
plt.title('上市年份分布')
plt.savefig(os.path.join(imgs_dir, '时间分析.png'))
# 3. 保修存在性与其他数据的关系，标好图例
plt.figure(figsize=(20, 10))
# 3.1 保修存在占比（1表示存在，0表示不存在，扇形图）
plt.subplot(2, 2, 1)
df['warranty_time_exist'].value_counts().plot.pie(autopct='%1.1f%%')
plt.legend(['无保修', '有保修'])
plt.ylabel('')
plt.title('保修存在占比')
# 3.2 保修存在与价格的关系
plt.subplot(2, 2, 2)
sns.boxplot(x='warranty_time_exist', y='price', data=df)
plt.xticks([0, 1], ['无保修', '有保修'])
plt.title('保修存在与价格的关系')
# 3.3 保修存在与里程的关系
plt.subplot(2, 2, 3)
sns.boxplot(x='warranty_time_exist', y='mileage', data=df)
plt.xticks([0, 1], ['无保修', '有保修'])
plt.title('保修存在与里程的关系')
# 3.4 保修存在与上牌时间的关系
plt.subplot(2, 2, 4)
sns.boxplot(x='warranty_time_exist', y='registration_time', data=df)
plt.xticks([0, 1], ['无保修', '有保修'])
plt.title('保修存在与上牌时间的关系')
plt.savefig(os.path.join(imgs_dir, '保修是否存在与其他数据的关系.png'))



