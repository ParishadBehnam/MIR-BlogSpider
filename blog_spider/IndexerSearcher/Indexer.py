from scipy import linalg
from elasticsearch import Elasticsearch
import json
from os import listdir
import numpy as np
import pickle


class MyElasticSearch:
    def __init__(self):
        pass

    def install(self):
        try:
            es = Elasticsearch(['localhost:9200'])
            print("Connected", es.info())
            es.indices.create(index='blog_index', ignore=[])
        except Exception as ex:
            print("Error:", ex)

    def delete_index(self, address='localhost:9200'):
        es = Elasticsearch([address])
        es.indices.delete(index='blog_index', ignore=[400, 404])

    def index(self, doc, id, doc_type='blog'):
        es = Elasticsearch(['localhost'], port=9200,)
        res = es.index(index="blog_index", doc_type=doc_type, id=id, body=doc)

    def get(self, id, doc_type='blog'):
        es = Elasticsearch(['localhost:9200'])
        res = es.get(index="blog_index", doc_type='blog', id=id)
        return res

    def delete(self, id, doc_type='blog'):
        es = Elasticsearch(['localhost'], port=9200,)
        res = es.delete(index="blog_index", doc_type=doc_type, id=id)

    def search(self, query):
        es = Elasticsearch(['localhost'], port=9200,)
        res = es.search(index="blog_index", body=query)
        return res

    def index_all(self, folder, address='localhost:9200'):
        all_blogs = {}
        posts_per_blog = {}
        es = Elasticsearch([address])
        for filename in listdir(folder):
            filename = filename[:-5]
            with open(folder+"/" + filename + ".json") as doc:
                js = json.loads(doc.read())
                if js['type'] == 'blog':
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

        for filename in listdir(folder):
            filename = filename[:-5]
            with open(folder+"/" + filename + ".json", 'r+') as post:
                js2 = json.loads(post.read())
                if js2['type'] == 'post':
                    d = all_blogs[js2['blog_url']]
                    p = d['posts'][d['post_ids'][js2['post_url']]]
                    comments = list()
                    if 'comment_urls' in js2:
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

        # self.make_matrix(alpha, es)
        with open('IDs.pkl', 'wb') as outp:
            pickle.dump(blog_ids, outp)
        print('Done')

    def normalize_matrix(selfa, matrix, alpha):
        l = len(matrix[0])
        for row in matrix:
            s = sum(row)
            for i in range(l):
                if s != 0:
                    row[i] = (((1 - alpha) * float(row[i])) / s) + (alpha / float(l))
                else:
                    row[i] = (1 / float(l))
        # for row in matrix:
        #     print(sum(row))
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

    def set_pagerank(self, alpha=0.1, address='localhost:9200'):
        es = Elasticsearch([address])
        matrix = self.make_matrix(alpha, es)
        # print(len(matrix))
        # with open('adjacency_matrix.pkl', 'rb') as inp:
        #     matrix = pickle.load(inp)

        v, eigenvectors, r = linalg.eig(matrix, left=True)
        eigenvector = (np.transpose(eigenvectors)[np.argmax(v)])
        eigenvector /= sum(eigenvector)
        for i in range(len(eigenvector)):
            res = es.get(index='blog_index', doc_type='blog', id=str(i + 1))
            res['_source']['blog']['page_rank'] = eigenvector[i].real
            es.index(index='blog_index', doc_type='blog', id=(i + 1), body=res['_source'])






















