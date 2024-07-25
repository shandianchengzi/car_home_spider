import scrapy

# 分析页面内容，可知包含的信息为“品牌”、“上市年份”、“车型”、“实物图”、“表显里程”、“上牌时间”、“价格”、“原厂保修时间”、“所属城市”和详细信息的访问链接。
class AutohomeItem(scrapy.Item):
    brand = scrapy.Field()
    year = scrapy.Field()
    model = scrapy.Field()
    mileage = scrapy.Field()
    registration_time = scrapy.Field()
    price = scrapy.Field()
    warranty_time = scrapy.Field()
    city = scrapy.Field()
    link = scrapy.Field()
    