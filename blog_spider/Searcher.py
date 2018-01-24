from elasticsearch import Elasticsearch


def search(blog_title, blog_title_w, post_title, post_title_w, post_content, post_content_w):
    es = Elasticsearch(['localhost'], port=9200,)
    res = es.search(index="blog_index", body=make_query(blog_title, blog_title_w, post_title, post_title_w, post_content,
                                                        post_content_w))
    return res


def show_urls(blog_title, blog_title_w, post_title, post_title_w, post_content, post_content_w):
    result = search(blog_title, blog_title_w, post_title, post_title_w, post_content, post_content_w)
    for hit in result['hits']['hits']:
        print(hit['_id']+' :')
        hit = hit['_source']
        print(hit['blog']['url'], hit['blog']['title'])


def make_query(blog_title, blog_title_w, post_title, post_title_w, post_content, post_content_w):
    q = {'query':
        {"bool":
            {"should": [
                { "match": {
                    "blog.title":  {
                        "query": blog_title,
                        "boost": blog_title_w
                    }
                }},
                { "match": {
                    "blog.posts.post_title":  {
                        "query": post_title,
                        "boost": post_title_w
                    }
                }},
                { "match": {
                    "blog.posts.post_content":  {
                        "query": post_content,
                        "boost": post_content_w
                    }
                }}]
            }
        }
    }
    return q
