from elasticsearch import Elasticsearch


def search(query):
    es = Elasticsearch(['localhost'], port=9200,)
    res = es.search(index="blog_index", body=query)
    return res


def show_urls(query):
    result = search(query)
    for hit in result['hits']['hits']:
        hit = hit['_source']
        print(hit['blog']['url'], hit['blog']['title'])


def make_query(blog_title, blog_title_w, post_title, post_title_w, post_content, post_content_w):
    pass
    # q = {'query': "bool": {
    #   "should": [
    #     { "match": {
    #         "title":  {
    #           "query": "War and Peace",
    #           "boost": 2
    #     }}},
    #     { "match": {
    #         "author":  {
    #           "query": "Leo Tolstoy",
    #           "boost": 2
    #     }}},}}
