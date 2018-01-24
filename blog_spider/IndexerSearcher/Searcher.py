from elasticsearch import Elasticsearch


def search(query, address):
    es = Elasticsearch([address])
    res = es.search(index="blog_index",
                    body={"size": 1000, 'query': make_query(query)})
    return res


def display_result(query, address='localhost:9200'):
    result = search(query, address)
    for hit in result['hits']['hits']:
        print(hit['_id'] + ' :')
        # print(hit['_score'])
        hit = hit['_source']
        print(hit['blog']['url'], '\n', hit['blog']['title'], '\n')
        counter = 0
        for post in hit['blog']['posts']:
            counter += 1
            print('post %d :' % counter)
            print(post['post_title'])
            print(post['post_content'])
        print('==============================================')


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
            "missing": 1
        }

    return q
