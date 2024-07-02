# 链家房产数据爬虫及分析器

本项目包含多个 Python 脚本，旨在从链家网站抓取、存储和分析房产数据。项目特点包括数据提取、数据库交互、数据分析和预测建模。

## 项目结构

- `spider_work.py`：包含从链家网站提取房产详细信息的网页爬取逻辑。使用 `requests` 进行 HTTP 请求和 `lxml` 进行 HTML 解析。
- `dbUtils.py`：管理数据库操作，如连接、插入和查询数据，使用 `pymongo` 与 MongoDB 交互。
- `analyse.py`：使用 `pandas`、`matplotlib` 和 `seaborn` 分析抓取的数据，生成关于房价、区域分布等的洞察。
- `ad_analyse.py`：利用 `scikit-learn` 和 `xgboost` 运用统计和机器学习模型根据区域、单价和房型等特征预测房产价格。

## 功能

- **数据爬取**：自动化抓取房产列表，包括价格、面积、社区细节等信息。
- **数据存储**：将抓取的数据有效存储到 MongoDB 数据库中。
- **数据分析**：对房产数据进行详细分析，包括价格分布、面积比较等统计洞察的可视化。
- **预测建模**：使用线性回归、随机森林和 XGBoost 模型预测基于各种属性的房产价格。

## 安装与设置

1. **克隆仓库：**
   ```
   git clone https://github.com/yourgithubusername/lianjia-scraper-analyzer.git
   ```
2. **安装依赖：**
   ```
   pip install -r requirements.txt
   ```

3. **配置：**
   - 确保系统已安装并正在运行 MongoDB。
   - 如有必要，更新 `dbUtils.py` 中的 MongoDB 连接细节。

4. **运行脚本：**
   - 执行 `spider_work.py` 开始数据爬取。
   - 运行 `ad_analyse.py` 和 `analyse.py` 进行数据分析和预测建模。

## 使用方法

```bash
python spider_work.py  # 爬取数据
python ad_analyse.py   # 分析爬取的数据
python analyse.py      # 进行预测建模
```
## 结果
![image](https://github.com/jerry609/lianjia_analyse/assets/83530782/53724175-0d35-4a87-9d5f-290aa479de02)
![image](https://github.com/jerry609/lianjia_analyse/assets/83530782/f6175865-8e92-45a8-b805-b38959d6d478)

