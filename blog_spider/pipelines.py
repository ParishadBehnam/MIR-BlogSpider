# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from blog_spider.items import Blog, Post


class BlogSpiderPipeline(object):
    def process_item(self, item, spider):
        return item


import json
import codecs


class JsonWithEncodingPipeline(object):

    def __init__(self):
        self.idx = 0
        # self.post_idx = 0

    def process_item(self, item, spider):
        if isinstance(item, Blog):
            self.idx += 1
            self.file = codecs.open('files/' + str(self.idx) + '.json', 'w', encoding='utf-8')
            line = json.dumps(dict(item), ensure_ascii=False)
            self.file.write(line)
            self.file.close()
            return item

        elif isinstance(item, Post):
            self.idx += 1
            self.file = codecs.open('files/' + str(self.idx) + '.json', 'w', encoding='utf-8')
            line = json.dumps(dict(item), ensure_ascii=False)
            self.file.write(line)
            self.file.close()
            return item

    def close_spider(self, spider):
        pass


