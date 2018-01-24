from os import listdir
from IndexerSearcher.Indexer import MyElasticSearch
from IndexerSearcher.Searcher import *
from elasticsearch import Elasticsearch

es = MyElasticSearch()
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
            state = int(input('Which one do you want?\n\t1)Phase1\n\t2)Phase2\n\t3)Phase3\n\t4)Phase4\n'))
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
            es_address = input('What is your elasticsearch address to delete?')
            # function call
            state = 0
        elif state == 2.2:
            folder = input('Enter the name of your crawled files\' folder\n')



# show_urls(make_query_for_search('سفر', 3, 'کاخ', 1, 'پایتخت مردم', 1, False))
# es.set_pagerank()
# es.set_pagerank()
cli()




