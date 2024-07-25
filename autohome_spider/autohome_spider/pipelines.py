# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv

class AutohomeSpiderPipeline:
    def open_spider(self, spider):
        self.file = open('autohome.csv', 'w', newline='', encoding='utf-8')
        self.writer = csv.DictWriter(self.file, fieldnames=['brand', 'year', 'model', 'mileage', 'registration_time', 'price', 'warranty_time', 'city', 'link'])
        # ['品牌', '上市年份', '车型', '表显里程（公里）', '上牌时间（年）', '价格（万）', '原厂保修时间', '所属城市', '链接']
        self.writer.writeheader()

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        # let item: {field: [value]} to {field: value}
        item = {k: v[0] for k, v in item.items()}
        self.writer.writerow(item)
        return item
