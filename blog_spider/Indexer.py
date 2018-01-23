from elasticsearch import Elasticsearch
import json
from os import listdir
import time
import numpy as np
import pickle
from scipy.linalg import eig

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
        blog_ids = {}
        for d in all_blogs.values():
            d.pop('post_ids')
            res = es.index(index="blog_index", doc_type='blog', id=cnt, body={"blog": d})
            blog_ids[d['url']] = cnt - 1
            cnt += 1

        with open('IDs.pkl', 'wb') as outp:
            pickle.dump(blog_ids, outp)
        print(len(all_blogs))

    def normalize_matrix(selfa, matrix, alpha):
        l = len(matrix[0])
        for row in matrix:
            s = sum(row)
            for i in range(l):
                if s != 0:
                    row[i] = (((1 - alpha) * float(row[i])) / s) + (alpha / float(l))
                else:
                    row[i] = (alpha / float(l))
        return matrix

    def make_matrix(self, alpha, es):
        with open('IDs.pkl', 'rb') as inp:
            blog_ids = pickle.load(inp)
        res = es.search(index="blog_index", body={"size": 1000, "query": {"match_all": {}}})
        matrix = [list(np.zeros(res['hits']['total'])) for _ in range(res['hits']['total'])]
        for d in (res['hits']['hits']):
            blog = (d['_source']['blog'])
            for p in blog['posts']:
                if 'post_comments' in p:
                    comments = p['post_comments']
                    for c in comments:
                        if c['comment_url'] in blog_ids:
                            matrix[blog_ids[c['comment_url']]][int(d['_id']) - 1] += 1

        matrix = self.normalize_matrix(matrix, alpha)
        with open('adjacency_matrix.pkl', 'wb') as outp:
            pickle.dump(matrix, outp)
        return matrix

    def set_pagerank(self, alpha=0.1):
        es = Elasticsearch(['localhost'], port=9200,)
        with open('adjacency_matrix.pkl', 'rb') as inp:
            matrix = pickle.load(inp)
        # matrix = self.make_matrix(alpha, es)
        # matrix = [[0.1, 0.9],[0.3, 0.7]]

        eigenvalues, eigenvectors = np.linalg.eig(matrix) #in kkojash eigen vector hesab mikone akhe?:(
        # masalan eigenvalues un chizie ke ma mikhaim:D
        for i in range(len(matrix)):
            res = es.get(index='blog_index', doc_type='blog', id=str(i + 1))
            res['_source']['blog']['page_rank'] = round(eigenvalues[i], 2) #ehtemalan serializationError bokhore
            # chon masalan 0.2 ro mikone 0.199999999...9 va nemitune indexesh kone:/
            es.index(index='blog_index', doc_type='blog', id=(i + 1), body=res)






















