from os import listdir
from Indexer import MyElasticSearch

es = MyElasticSearch()
# print(len(listdir('blogs')))
es.delete_index()
es.index_all()
# es.delete_index()
# es.install()
# es.index(doc, 152)
# print(es.get(982))