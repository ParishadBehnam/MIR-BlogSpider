import pickle

import logging
import scrapy
import sys
import re

from blog_spider.items import Blog, Post, Post_full_content
from bs4 import BeautifulSoup


class BlogSpider(scrapy.Spider):
    name = "blogs"
    n = 0
    crawled = 0

    def __init__(self, urls=None, n=None, *args, **kwargs):
        logging.getLogger('scrapy').setLevel(logging.WARNING)
        super(BlogSpider, self).__init__(*args, **kwargs)
        self.start_urls = urls.split(",")

        BlogSpider.n = n
        BlogSpider.crawled = 0

    def parse(self, response):
        if BlogSpider.crawled < BlogSpider.n:
            soup = BeautifulSoup(response.text, 'xml')

            blog_name = soup.title.string
            blog_url = soup.link.string
            blog = Blog(type='blog', blog_name=blog_name, blog_url=blog_url)

            posts = soup.select("item")
            i = 0
            for post in posts:
                i += 1
                if i > 5:
                    break

                post_url = post.link.string

                blog['post_url_' + str(i)] = post.link.string
                blog['post_title_' + str(i)] = post.title.string

                desc = post.description.string
                soup_txt = BeautifulSoup(desc, 'xml')
                blog['post_content_' + str(i)] = soup_txt.get_text()

                next_page = post.link.string
                if next_page is not None:
                    res = response.follow(next_page, callback=self.parse_post)
                    res.meta['post_url'] = post_url
                    res.meta['blog_url'] = blog_url
                    yield res

                    res_content = response.follow(next_page, callback=self.parse_content, priority=10, dont_filter=True)
                    res_content.meta['blog'] = blog
                    res_content.meta['index'] = i
                    yield res_content

            blog['max_post'] = i - 1

            yield blog

    def parse_post(self, response):

        post_url = response.meta['post_url']
        blog_url = response.meta['blog_url']
        post = Post(type="post", blog_url=blog_url, post_url=post_url)
        comments = []

        soup = BeautifulSoup(response.text, 'xml')
        comm_el = soup.find("a", attrs={"name": "comments"})

        if comm_el is not None:
            comment_parent = soup.find("a", attrs={"name": "comments"}).parent
            child_comments = comment_parent.findChildren()
            for child in child_comments:
                a_tag = child.find("a")
                p = re.compile("^(http://)?[^/]*\.blog\.ir(/)?$")

                if a_tag is not None and a_tag.has_attr('href') and p.match(a_tag['href']) is not None:
                    a_tag_el = a_tag['href'] if a_tag['href'][-1] == "/" else a_tag['href'] + "/"
                    http_reg = re.compile("^http(s)?://.*")
                    a_tag_el = a_tag_el if http_reg.match(a_tag_el) is not None else "http://" + a_tag_el

                    if a_tag_el not in comments:
                        comments.append(a_tag_el)
                        if BlogSpider.crawled < BlogSpider.n:
                            yield response.follow(a_tag_el + "rss", callback=self.parse, priority=10)

            post['comment_urls'] = comments
        yield post

    def parse_content(self, response):
        soup = BeautifulSoup(response.text, 'xml')
        blog = response.meta['blog']
        index = response.meta['index']

        if soup.find("div", class_=re.compile("^post$|^post ")) is not None:
            desc = soup.find("div", class_=re.compile("^post$|^post "))

            if desc.find("a", attrs={"name": "comments"}) is not None:
                for el in desc.find("a", attrs={"name": "comments"}).fetchNextSiblings():
                    el.decompose()

            full_content = desc.get_text()
        else:
            full_content = ""

        post_content = Post_full_content(index=index, blog=blog, content=full_content)

        yield post_content
