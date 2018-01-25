# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BlogSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Blog(scrapy.Item):
    type = scrapy.Field()
    max_post = scrapy.Field()
    blog_name = scrapy.Field()
    blog_url = scrapy.Field()

    post_url_1 = scrapy.Field()
    post_title_1 = scrapy.Field()
    post_content_1 = scrapy.Field()
    post_full_content_1 = scrapy.Field()

    post_url_2 = scrapy.Field()
    post_title_2 = scrapy.Field()
    post_content_2 = scrapy.Field()
    post_full_content_2 = scrapy.Field()

    post_url_3 = scrapy.Field()
    post_title_3 = scrapy.Field()
    post_content_3 = scrapy.Field()
    post_full_content_3 = scrapy.Field()

    post_url_4 = scrapy.Field()
    post_title_4 = scrapy.Field()
    post_content_4 = scrapy.Field()
    post_full_content_4 = scrapy.Field()

    post_url_5 = scrapy.Field()
    post_title_5 = scrapy.Field()
    post_content_5 = scrapy.Field()
    post_full_content_5 = scrapy.Field()


class Post(scrapy.Item):

    type= scrapy.Field()
    blog_url = scrapy.Field()
    post_url = scrapy.Field()
    comment_urls = scrapy.Field()

class Post_full_content(scrapy.Item):
    index = scrapy.Field()
    content = scrapy.Field()
    blog = scrapy.Field()
