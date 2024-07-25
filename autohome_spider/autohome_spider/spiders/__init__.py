import scrapy
from scrapy.loader import ItemLoader
from autohome_spider.items import AutohomeItem
import re
import lxml

def getNumberAndFloat(text):
    result = re.findall(r'\d+\.?\d*', text)
    if len(result) == 0:
        with open('error.log', 'a', encoding='utf-8') as f:
            f.write(text + '\n')
        return ""
    return result[0]

# 产品库的二手车页面中，页码也在链接中。比如a0_0msdgscncgpi1lto2csp1ex/对应第一页，a0_0msdgscncgpi1lto2csp2ex/对应第二页。
class AutohomeSpider(scrapy.Spider):
    name = 'autohome_spider'
    allowed_domains = ['autohome.com.cn']
    base_url = 'https://car.autohome.com.cn/2sc/dalian/a0_0msdgscncgpi1lto2csp{}ex/'
    page = 1
    start_urls = ['https://car.autohome.com.cn/2sc/dalian/a0_0msdgscncgpi1lto2csp1ex/']

    def parse(self, response):
        xml = lxml.etree.HTML(response.text)
        piclist = xml.xpath('//div[@class="piclist"]/ul/li')
        if len(piclist) == 0 or self.page > 100: # max page 100
            return
        for car in piclist:
            try:
                l = ItemLoader(item=AutohomeItem())
                title = car.xpath('div[@class="title"]/a/text()')[0]
                title_href = car.xpath('div[@class="title"]/a/@href')[0]
                somethings = title.split(' ', 2)
                if len(somethings) != 3:
                    with open('error.log', 'a') as f:
                        f.write(title + '\n')
                    continue
                # 获得icon_list里所有a标签的title属性并拼接非空的为字符串
                icon_list = car.xpath('div[@class="icon-list"]/a')
                city = car.xpath('div[@class="icon-list"]/span/span/text()')[0]
                icons_info = []
                for icon in icon_list:
                    icon_info = icon.xpath('@title')
                    if icon_info:
                        icons_info.extend(icon_info)
                icons_info = ', '.join(icons_info)
                # 用ItemLoader加载数据
                l.add_value('brand', somethings[0])
                l.add_value('year', somethings[1])
                l.add_value('model', somethings[2])
                l.add_value('mileage', getNumberAndFloat(car.xpath('*/div[@class="detail-l"]/p[1]/text()')[0]))
                l.add_value('registration_time', getNumberAndFloat(car.xpath('*/div[@class="detail-l"]/p[2]/text()')[0]))
                l.add_value('price', car.xpath('*/div[@class="detail-r"]/span/text()'))
                l.add_value('warranty_time', icons_info)
                l.add_value('city', city)
                l.add_value('link', "https:" + title_href)
                yield l.load_item()
            except Exception as e:
                # skip no full information car
                pass

        # 下一页
        self.page += 1
        new_url = self.base_url.format(self.page)
        yield scrapy.Request(new_url, callback=self.parse)