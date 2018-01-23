from os import listdir
from Indexer import MyElasticSearch
from elasticsearch import Elasticsearch

es = MyElasticSearch()
# print(len(listdir('blogs')))
# es.delete_index()
# es.index_all()
# es.delete_index()
# es.install()
# es.index(doc, 152)
# print(es.get(982))

# res = es.make_matrix(0.1, Elasticsearch(['localhost'], port=9200,))
# print(res)

es.set_pagerank()