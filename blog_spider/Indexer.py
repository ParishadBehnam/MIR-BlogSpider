from elasticsearch import Elasticsearch
import json
from os import listdir
import time


class MyElasticSearch:
    def __init__(self):
        pass

    def install(self):
        try:
            es = Elasticsearch(['localhost'], port=9200,)
            print("Connected", es.info())
            es.indices.create(index='blog_index', ignore=[])
        except Exception as ex:
            print("Error:", ex)

    def delete_index(self):
        es = Elasticsearch()
        es.indices.delete(index='blog_index', ignore=[])

    def index(self, doc, id, doc_type='blog'):
        es = Elasticsearch(['localhost'], port=9200,)
        res = es.index(index="blog_index", doc_type=doc_type, id=id, body=doc)

    def get(self, id, doc_type='blog'):
        es = Elasticsearch(['localhost'], port=9200,)
        res = es.get(index="blog_index", doc_type='blog', id=id)
        return res

    def delete(self, id, doc_type='blog'):
        es = Elasticsearch(['localhost'], port=9200,)
        res = es.delete(index="blog_index", doc_type=doc_type, id=id)

    def index_all(self):
        all_blogs = {}
        posts_per_blog = {}
        es = Elasticsearch(['localhost'], port=9200,)
        # cnt = 0
        for filename in listdir('blogs'):
            filename = filename[:-5]
            with open("blogs/" + filename + ".json") as doc:
                js = json.loads(doc.read())
                d = dict()
                d["url"] = js["blog_url"]
                d["title"] = js["blog_name"]
                posts_per_blog[js['blog_url']] = []

                posts = list()
                post_ids = dict()
                for post_id in range(1, 6):
                    if "post_url_" + str(post_id) in js:
                        p = dict()
                        p["post_url"] = js["post_url_" + str(post_id)]
                        p["post_title"] = js["post_title_" + str(post_id)]
                        p["post_content"] = js["post_content_" + str(post_id)]
                        post_ids[js["post_url_" + str(post_id)]] = (post_id - 1)
                        posts.append(p)
                d['post_ids'] = post_ids
                d['posts'] = posts
                # if d['url'] in all_blogs:
                #     print(filename, d['url'])
                all_blogs[d['url']] = d

        for filename in listdir('posts'):
            filename = filename[:-5]
            with open("posts/" + filename + ".json", 'r+') as post:
                js2 = json.loads(post.read())
                d = all_blogs[js2['blog_url']]
                p = d['posts'][d['post_ids'][js2['post_url']]]
                comments = list()
                for c in js2["comment_urls"]:
                    comments.append({"comment_url": c})
                if len(comments) > 0:
                    p["post_comments"] = comments

        cnt = 1
        for d in all_blogs.values():
            d.pop('post_ids')
            # print(cnt, {"blog": d})
            res = es.index(index="blog_index", doc_type='blog', id=cnt, body={"blog": d})
            cnt += 1

        print(len(all_blogs))
