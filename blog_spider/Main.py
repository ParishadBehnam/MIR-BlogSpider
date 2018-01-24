from os import listdir
from IndexerSearcher.Indexer import MyElasticSearch
from IndexerSearcher.Searcher import *
from elasticsearch import Elasticsearch

# print(len(listdir('blogs')))
# es.delete_index()
# es.index_all()
# es.delete_index()
# es.install()
# es.index(doc, 152)
# print(es.get(982))
# es.set_pagerank()

# print(es.search({'query': {'nested':{'path':'blog','query':{'match':{'title':'درستان | عکس و تصاویر مذهبی'}}}}}))
# print(es.search({'query': {'match':{'blog.title':'زندگی', }}}))
# res = es.make_matrix(0.1, Elasticsearch(['localhost'], port=9200,))

# print(res)

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
            state = int(input('Which one do you want?\n\t1)Phase1\n\t2)Phase2\n\t3)Phase3\n\t4)Phase4\n\t5)Exit\n'))
        elif state == 1:
            ls = input('Enter the base links[separated by \',\']\n')
            links = ls.split(',')
            in_degree = int(input('Enter the in_degree\n'))
            n = int(input('Enter the number of crawled weblogs\n'))
            #function call
            state = 0
        elif state == 2:
            state = 2.1 if input('Which one do you want?\n\t1)Delete the whole index\n\t2)Make the index\n') == '1'\
                else 2.2
        elif state == 2.1:
            es = MyElasticSearch()
            es_address = input('What is your elasticsearch address to delete?\n')
            es.delete_index(es_address)
            state = 0
        elif state == 2.2:
            es = MyElasticSearch()
            es_address = input('What is your elasticsearch address?\n')
            folder = input('Enter the name of your crawled files\' folder\t')
            es.index_all(folder, es_address)
            state = 0
        elif state == 3:
            es = MyElasticSearch()
            es_address = input('What is your elasticsearch address?\n')
            alpha = input('Enter yout desired alpha\t')
            es.set_pagerank(alpha=alpha, address=es_address)
            state = 0
        elif state == 4:
            es_address = input('What is your elasticsearch address?\n')
            blog_title = input('Type your blog title field or leave it blank if not important!\n')
            blog_title_w = float(input('Enter the weight of the blog title field\t'))
            post_title = input('Type your post title field or leave it blank if not important!\n')
            post_title_w = float(input('Enter the weight of the post title field\t'))
            post_content = input('Type your post content field or leave it blank if not important!\n')
            post_content_w = float(input('Enter the weight of the post content field\t'))
            page_rank = True if input('Do you want page_rank to affect the result? y/n\t') == 'y' else False
            display_result(make_query_for_search(blog_title, blog_title_w, post_title, post_title_w,
                                                 post_content, post_content_w, page_rank), es_address)
            state = 0
        elif state == 5:
            return




# show_urls(display_result('سفر', 3, 'کاخ', 1, 'پایتخت مردم', 1, False))
# es.set_pagerank()
# es.set_pagerank()
cli()
# print(es.get(2))



