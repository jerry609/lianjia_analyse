import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['font.family'] = ['SimHei']  # 或 'Microsoft YaHei'
plt.rcParams['axes.unicode_minus'] = False  # 确保负号正确显示

# 加载数据
data_path = 'D:\\Pycharm_pro\\Spider-Pro\\pythonProject2\\lianjia2\\spyLianjia.houseInfo.json'
df = pd.read_json(data_path)

# 数据清洗和转换
df['房屋总价'] = df['房屋总价'].str.replace('万', '').astype(float)
df['建筑面积'] = df['建筑面积'].str.replace('㎡', '').astype(float)

# 处理 '单位价格' 列
df['单位价格'] = pd.to_numeric(df['单位价格'], errors='coerce')

# 1. 房价分布
plt.figure(figsize=(10, 6))
sns.histplot(df['房屋总价'], bins=30, kde=True)
plt.title('房屋总价分布')
plt.xlabel('总价（万元）')
plt.ylabel('数量')
plt.show()

# 2. 建筑面积与房屋总价关系
plt.figure(figsize=(10, 6))
sns.scatterplot(x='建筑面积', y='房屋总价', data=df)
plt.title('建筑面积与房屋总价关系图')
plt.xlabel('建筑面积 (平方米)')
plt.ylabel('房屋总价 (万元)')
plt.show()

# 3. 各行政区域的房价比较
plt.figure(figsize=(12, 6))
sns.barplot(x='行政区域', y='房屋总价', data=df)
plt.title('各行政区域的平均房价')
plt.xlabel('行政区域')
plt.xticks(rotation=45)
plt.ylabel('平均房屋总价 (万元)')
plt.show()

# 4. 装修情况对房价的影响
plt.figure(figsize=(10, 6))
sns.boxplot(x='装修情况', y='房屋总价', data=df)
plt.title('装修情况与房屋总价的关系')
plt.xlabel('装修情况')
plt.ylabel('房屋总价 (万元)')
plt.show()

# 5. 户型分析
plt.figure(figsize=(10, 6))
df['房屋户型'].value_counts().plot(kind='pie', autopct='%1.1f%%')
plt.title('户型分布')
plt.show()

# 6. 单价分布
plt.figure(figsize=(10, 6))
sns.histplot(df['单位价格'].dropna(), bins=30, kde=True)
plt.title('单价分布')
plt.xlabel('单价（元/平方米）')
plt.ylabel('数量')
plt.show()

# 7. 单价与总价关系
plt.figure(figsize=(10, 6))
sns.scatterplot(x='单位价格', y='房屋总价', data=df.dropna(subset=['单位价格']))
plt.title('单价与总价关系')
plt.xlabel('单价（元/平方米）')
plt.ylabel('总价（万元）')
plt.show()

# 8. 数据统计摘要
summary = df[['房屋总价', '建筑面积', '单位价格']].describe()
print(summary)