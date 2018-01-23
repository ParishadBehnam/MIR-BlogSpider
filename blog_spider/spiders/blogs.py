import scrapy

from blog_spider.items import Blog, Post
from bs4 import BeautifulSoup


class BlogSpider(scrapy.Spider):
    name = "blogs"

    def __init__(self, urls=None, n=None, *args, **kwargs):
        super(BlogSpider, self).__init__(*args, **kwargs)
        self.start_urls = urls.split(",")
        self.n = int(n)
        self.crawled = 0

    def parse(self, response):
        if self.crawled < self.n:
            soup = BeautifulSoup(response.text, 'xml')
            self.crawled += 1

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

            yield blog

    def parse_post(self, response):

        post_url = response.meta['post_url']
        blog_url = response.meta['blog_url']
        post = Post(type="post", blog_url=blog_url, post_url=post_url)
        comments = []

        soup = BeautifulSoup(response.text, 'xml')

        comment_parent = soup.find("a", attrs={"name": "comments"}).parent
        child_comments = comment_parent.findChildren()
        for child in child_comments:
            a_tag = child.find("a")
            if a_tag is not None and a_tag.has_attr('href'):
                if (".blog.ir" in a_tag['href']):
                    if ("http:" not in a_tag['href']):
                        if ("http:" + a_tag['href'] not in comments):
                            page = "http:" + a_tag['href']
                            comments.append(page)
                            if (self.crawled) < self.n:
                                yield response.follow(page + "/rss", callback=self.parse)

                    else:
                        if (a_tag['href'] not in comments):
                            comments.append(a_tag['href'])
                            if (self.crawled) < self.n:
                                yield response.follow(a_tag['href'] + "/rss", callback=self.parse)

        post['comment_urls'] = comments
        yield post
