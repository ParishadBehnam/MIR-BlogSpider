from elasticsearch import Elasticsearch


def search(query):
    es = Elasticsearch(['localhost'], port=9200, )
    res = es.search(index="blog_index",
                    body={"size": 1000, 'query': make_query(query)})
    return res


def show_urls(query):
    result = search(query)
    for hit in result['hits']['hits']:
        print(hit['_id'] + ' :')
        print(hit['_score'])
        hit = hit['_source']
        print(hit['blog']['url'], hit['blog']['title'], hit['blog']['page_rank'])


def make_query(query):
    q = {'function_score':
        {
            'query': {"bool":
                {"should": [
                    {"match": {
                        "blog.title": {
                            "query": query['blog_title'][0],
                            "boost": query['blog_title'][1]
                        }
                    }},
                    {"match": {
                        "blog.posts.post_title": {
                            "query": query['post_title'][0],
                            "boost": query['post_title'][1]
                        }
                    }},
                    {"match": {
                        "blog.posts.post_content": {
                            "query": query['post_content'][0],
                            "boost": query['post_content'][1]
                        }
                    }}]
                }
            },

        }}
    if query['page_rank']:
        q['function_score']['boost_mode'] = 'sum'
        q['function_score']['field_value_factor'] = {
            "field": "blog.page_rank",
            "factor": 100,
            # "modifier": "sqrt",
            "missing": 1
        }

    return q
