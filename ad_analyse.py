import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb
from sklearn.metrics import mean_squared_error, r2_score
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
df['单位价格'] = pd.to_numeric(df['单位价格'], errors='coerce')

# 选择特征
features = ['建筑面积', '单位价格', '房屋户型', '所在楼层', '装修情况', '建筑类型', '行政区域']
target = '房屋总价'

# 处理缺失值
df = df.dropna(subset=features + [target])

# 编码分类变量
le = LabelEncoder()
for feature in ['房屋户型', '所在楼层', '装修情况', '建筑类型', '行政区域']:
    df[feature] = le.fit_transform(df[feature].astype(str))

# 准备数据
X = df[features]
y = df[target]

# 分割训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 创建并训练模型
lr_model = LinearRegression()
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
xgb_model = xgb.XGBRegressor(random_state=42)

lr_model.fit(X_train, y_train)
rf_model.fit(X_train, y_train)
xgb_model.fit(X_train, y_train)

# 进行预测
lr_pred = lr_model.predict(X_test)
rf_pred = rf_model.predict(X_test)
xgb_pred = xgb_model.predict(X_test)

# 评估模型
models = {'线性回归': (lr_pred, lr_model), '随机森林': (rf_pred, rf_model), 'XGBoost': (xgb_pred, xgb_model)}

for name, (pred, model) in models.items():
    mse = mean_squared_error(y_test, pred)
    r2 = r2_score(y_test, pred)
    print(f"\n{name}模型:")
    print(f"均方误差: {mse}")
    print(f"R2 分数: {r2}")

# 可视化预测结果
plt.figure(figsize=(12, 6))
for name, (pred, _) in models.items():
    plt.scatter(y_test, pred, alpha=0.5, label=name)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.xlabel('实际价格')
plt.ylabel('预测价格')
plt.title('房价预测对比')
plt.legend()
plt.show()

# 特征重要性
for name, (_, model) in models.items():
    if hasattr(model, 'feature_importances_'):
        feature_importance = pd.DataFrame({'feature': features, 'importance': model.feature_importances_})
        feature_importance = feature_importance.sort_values('importance', ascending=False)
        plt.figure(figsize=(10, 6))
        sns.barplot(x='importance', y='feature', data=feature_importance)
        plt.title(f'{name}特征重要性')
        plt.show()

# 预测新房价
new_house = pd.DataFrame({
    '建筑面积': [100],
    '单位价格': [20000],
    '房屋户型': [le.transform(['3室2厅1厨1卫'])[0] if '3室2厅1厨1卫' in le.classes_ else -1],
    '所在楼层': [le.transform(['中楼层'])[0] if '中楼层' in le.classes_ else -1],
    '装修情况': [le.transform(['精装'])[0] if '精装' in le.classes_ else -1],
    '建筑类型': [le.transform(['板楼'])[0] if '板楼' in le.classes_ else -1],
    '行政区域': [le.transform(['江宁'])[0] if '江宁' in le.classes_ else -1]
})

for name, (_, model) in models.items():
    predicted_price = model.predict(new_house)
    print(f"{name}预测价格: {predicted_price[0]:.2f}万元")