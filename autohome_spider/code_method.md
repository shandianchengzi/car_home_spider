### 项目：汽车之家数据爬取、清洗与可视化

#### 一、Scrapy框架数据爬取

##### 使用Scrapy框架进行数据爬取

1. **创建Scrapy项目**：在命令行中执行`scrapy startproject autohome_spider`，创建一个新的Scrapy项目。

2. **定义Item**：在`items.py`文件中定义数据模型，用于存储爬取的汽车信息。

   ```python
   import scrapy

   class AutohomeItem(scrapy.Item):
       brand = scrapy.Field()
       model = scrapy.Field()
       price = scrapy.Field()
       fuel_consumption = scrapy.Field()
       engine_type = scrapy.Field()
   ```

3. **编写Spider**：在`spiders`目录下创建一个Spider，用于爬取数据。

   ```python
   import scrapy
   from autohome_spider.items import AutohomeItem

   class AutohomeSpider(scrapy.Spider):
       name = 'autohome'
       allowed_domains = ['autohome.com.cn']
       start_urls = ['https://www.autohome.com.cn/grade/carhtml/A.html']

       def parse(self, response):
           for car in response.css('dl.car-list-text'):
               item = AutohomeItem()
               item['brand'] = car.css('dt a::text').get()
               item['model'] = car.css('dd.h3-tit a::text').get()
               item['price'] = car.css('dd.main-price::text').get().strip()
               yield item
   ```

4. **设置Pipelines**：在`settings.py`中启用Pipelines，并在`pipelines.py`中定义Pipelines，用于处理爬取的数据。

   ```python
   # settings.py
   ITEM_PIPELINES = {
       'autohome_spider.pipelines.AutohomePipeline': 300,
   }

   # pipelines.py
   import csv

   class AutohomePipeline:
       def open_spider(self, spider):
           self.file = open('autohome.csv', 'w', newline='', encoding='utf-8')
           self.writer = csv.DictWriter(self.file, fieldnames=['brand', 'model', 'price', 'fuel_consumption', 'engine_type'])
           self.writer.writeheader()

       def close_spider(self, spider):
           self.file.close()

       def process_item(self, item, spider):
           self.writer.writerow(item)
           return item
   ```

#### 二、Pandas数据清洗与可视化

##### 使用Pandas进行数据清洗
数据清洗的主要目的是为了去掉重复和空数据、纠正错误。我之前的解析代码中忽略了品牌的名称中可能携带空格，导致最终解析出来的结果，品牌名称被分割到下一列中，出现错误。数据清洗的过程中可以纠正。

```python
import re

df.drop_duplicates(inplace=True) # 去重
df.dropna(subset=['brand'], inplace=True) # 去掉品牌为空的数据
# 合并前三列的数据形成字符串，用正则重新解析
df['brand'] = df['brand'] + ' ' + df['model'] + ' ' + df['price']
df['year'] = df['year'].replace('款', '', regex=True)
# df.columns = ['品牌', '上市年份', '车型', '表显里程（公里）', '上牌时间（年）', '价格（万）', '原厂保修时间', '所属城市', '链接']
df.to_csv(result_path, index=False, encoding='gbk')
```

1. **读取CSV文件**：使用Pandas读取由Scrapy爬取并存储的CSV文件。

   ```python
   import pandas as pd

   df = pd.read_csv('autohome.csv')
   ```

2. **数据清洗**：处理缺失值、重复项和异常值。

   ```python
   df.drop_duplicates(inplace=True)
   df.dropna(inplace=True)
   ```

3. **数据转换**：将价格从字符串转换为数值型。

   ```python
   df['price'] = df['price'].str.replace('万', '').astype(float)
   ```

##### 使用Pandas进行数据可视化

1. **导入可视化库**：使用Matplotlib或Seaborn进行数据可视化。

   ```python
   import matplotlib.pyplot as plt
   import seaborn as sns
   ```

2. **价格分布直方图**：查看不同品牌汽车的价格分布。

   ```python
   sns.histplot(df['price'], kde=True)
   plt.title('Price Distribution of Cars')
   plt.show()
   ```

3. **品牌价格箱线图**：对比不同品牌汽车的价格范围。

   ```python
   sns.boxplot(x='brand', y='price', data=df)
   plt.xticks(rotation=90)
   plt.title('Price Range by Brand')
   plt.show()
   ```

通过上述步骤，我们不仅完成了数据的爬取和存储，还进行了有效的数据清洗和可视化分析，为后续的数据挖掘和业务决策提供了有力支持。