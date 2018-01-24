from os import listdir
from Indexer import MyElasticSearch
from Searcher import *
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

show_urls('', 3, 'کاخ', 1, 'پایتخت مردم', 1)

# es.set_pagerank()