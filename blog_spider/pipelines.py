# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from blog_spider.items import Blog, Post, Post_full_content
from blog_spider.spiders.blogs import BlogSpider


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
            # return item
            pass

        elif isinstance(item, Post):
            self.idx += 1
            self.file = codecs.open('blogs/' + str(self.idx) + '.json', 'w', encoding='utf-8')
            line = json.dumps(dict(item), ensure_ascii=False)
            self.file.write(line)
            self.file.close()
            return item

        elif isinstance(item, Post_full_content):
            blog = item['blog']
            idx = item['index']
            blog['post_full_content_' + str(idx)] = item['content']
            blog['max_post'] -= 1

            if blog['max_post'] == 0:
                BlogSpider.crawled += 1
                self.idx += 1
                self.file = codecs.open('blogs/' + str(self.idx) + '.json', 'w', encoding='utf-8')
                blog_dict = dict(blog)
                blog_dict.pop('max_post')
                line = json.dumps(blog_dict, ensure_ascii=False)
                self.file.write(line)
                self.file.close()
                return item



    def close_spider(self, spider):
        pass


