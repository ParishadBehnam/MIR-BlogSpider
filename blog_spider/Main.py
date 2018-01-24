from os import listdir
from blog_spider.IndexerSearcher.Indexer import MyElasticSearch
from blog_spider.IndexerSearcher.Searcher import *
from elasticsearch import Elasticsearch

es = MyElasticSearch()
# print(len(listdir('blogs')))
# es.delete_index()
# es.index_all()
# es.delete_index()
# es.install()
# es.index(doc, 152)
# print(es.get(982))

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

show_urls(make_query_for_search('', 3, 'کاخ', 1, 'پایتخت مردم', 1, False))
# es.set_pagerank()
# es.set_pagerank()






