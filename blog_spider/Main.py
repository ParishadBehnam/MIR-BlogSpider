from IndexerSearcher.Indexer import MyElasticSearch
from IndexerSearcher.Searcher import *


from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from blog_spider import settings as my_settings
from blog_spider.spiders.blogs import BlogSpider

class bcolors:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def make_query_for_search(blog_title, blog_title_w, post_title, post_title_w, post_content, post_content_w, page_rank):
    query = dict()
    query['blog_title'] = [blog_title, blog_title_w]
    query['post_title'] = [post_title, post_title_w]
    query['post_content'] = [post_content, post_content_w]
    query['page_rank'] = page_rank
    return query


def cli():
    state = 0

    while True:
        if state == 0:
            state = int(input(
                bcolors.BOLD + 'Which one do you want?' + bcolors.ENDC + '\n\t1)Phase1\n\t2)Phase2\n\t3)Phase3\n\t4)Phase4\n\t5)Exit\n'))
        elif state == 1:
            ls = input('Enter the base links[separated by \',\']\n')
            ls = ls if ls != "" else 'http://complex-life.blog.ir/rss/,http://aghagol.blog.ir/rss/'
            in_degree = int(input('Enter the in_degree\n'))
            n = int(input('Enter the number of crawled weblogs\n'))

            crawler_settings = Settings()
            crawler_settings.setmodule(my_settings)
            process = CrawlerProcess(settings=crawler_settings)
            process.crawl(BlogSpider, urls=ls, n=n)
            process.start()

            print(bcolors.OKGREEN + '>>>Done\n' + bcolors.ENDC)
            state = 0
        elif state == 2:
            state = 2.1 if input(
                bcolors.BOLD + 'Which one do you want?' + bcolors.ENDC + '\n\t1)Delete the whole index\n\t2)Make the index\n') == '1' \
                else 2.2
        elif state == 2.1:
            es = MyElasticSearch()
            es_address = input('What is your elasticsearch address to delete? [leave in blank if you want it to be localhost:9200]\n')
            es_address = 'localhost:9200' if es_address == '' else es_address
            es.delete_index(es_address)
            print(bcolors.OKGREEN + '>>>Done\n' + bcolors.ENDC)
            state = 0
        elif state == 2.2:
            es = MyElasticSearch()
            es_address = input('What is your elasticsearch address? [leave in blank if you want it to be localhost:9200]\n')
            es_address = 'localhost:9200' if es_address == '' else es_address
            folder = input('Enter the name of your crawled blogs\' folder\t')
            es.index_all(folder, es_address)
            print(bcolors.OKGREEN + '>>>Done\n' + bcolors.ENDC)
            state = 0
        elif state == 3:
            es = MyElasticSearch()
            es_address = input('What is your elasticsearch address? [leave in blank if you want it to be localhost:9200]\n')
            es_address = 'localhost:9200' if es_address == '' else es_address
            alpha = input('Enter yout desired alpha\t')
            es.set_pagerank(alpha=float(alpha), address=es_address)
            print(bcolors.OKGREEN + '>>>Done\n' + bcolors.ENDC)
            state = 0
        elif state == 4:
            es_address = input('What is your elasticsearch address? [leave in blank if you want it to be localhost:9200]\n')
            es_address = 'localhost:9200' if es_address == '' else es_address
            blog_title = input('Type your blog title field or leave it blank if not important!\n')
            blog_title_w = float(input('Enter the weight of the blog title field\t'))
            post_title = input('Type your post title field or leave it blank if not important!\n')
            post_title_w = float(input('Enter the weight of the post title field\t'))
            post_content = input('Type your post content field or leave it blank if not important!\n')
            post_content_w = float(input('Enter the weight of the post content field\t'))
            page_rank = True if input('Do you want page_rank to affect the result? y/n\t') == 'y' else False
            display_result(make_query_for_search(blog_title, blog_title_w, post_title, post_title_w,
                                                 post_content, post_content_w, page_rank), es_address)
            print(bcolors.OKGREEN + '>>>Done\n' + bcolors.ENDC)
            state = 0
        elif state == 5:
            return


# starts from this point
cli()
