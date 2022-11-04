from gensim.similarities import SparseMatrixSimilarity
from gensim.corpora import Dictionary
from gensim.models import TfidfModel
import numpy as np
import pickle

class TFIDFSimilarity:
    def __init__(self):
        pass

    def train(self, data):
        '''
        训练模型，需转入待匹配列表
        '''
        texts = data
        self.dictionary = Dictionary(texts)
        print("Dictionary built.")
        corpus = [self.dictionary.doc2bow(text) for text in texts]
        print("corpus built.")
        self.tfidf = TfidfModel(corpus)
        print("tf-idf model built.")

    def save_tfidf(self, path):
        with open(path+"dictionary.pickle", "wb") as f:
            pickle.dump(self.dictionary, f)
        with open(path + "tfidf_model.pickle", "wb") as f:
            pickle.dump(self.tfidf, f)

    def load_tfidf(self, path):
        with open(path+"dictionary.pickle", "rb") as f:
            self.dictionary = pickle.load(f)
        with open(path + "tfidf_model.pickle", "rb") as f:
            self.tfidf = pickle.load(f)

    def jaccard(self, a, b):
        return len(set(a).intersection(set(b))) / len(set(a).union(set(b)))

    def compare_similarity(self, string_a, string_b, max_thres):
        kw_vector_a = self.dictionary.doc2bow(string_a.split(" "))
        tf_kw_a = self.tfidf[kw_vector_a]
        tf_kw_a.sort(key = lambda x : x[1], reverse=True)
        a_list = [pair[0] for pair in tf_kw_a]
        #文本在20个字符以内则全保留
        a_list = a_list[:] if len(a_list) <= 20 else a_list[:int(max_thres*len(a_list))]
        #a_list = a_list[:int(max_thres*len(a_list))]

        kw_vector_b = self.dictionary.doc2bow(string_b.split(" "))
        tf_kw_b = self.tfidf[kw_vector_b]
        tf_kw_b.sort(key=lambda x: x[1], reverse=True)
        b_list = [pair[0] for pair in tf_kw_b]
        b_list = b_list[:] if len(b_list) <= 20 else b_list[:int(max_thres*len(b_list))]
        #b_list = b_list[:int(max_thres * len(b_list))]

        j_simi = self.jaccard(a_list,b_list)
        print(j_simi)
        return j_simi

    # 输入原始文本，返回经tfidf处理后按照特征值映射（与原字不同）由高到低排序的列表数组（去重）
    def text_2_tfidf_characteristic_value(self, original_string):
        kw_vector = self.dictionary.doc2bow(original_string.split(" "))
        tf_kw = self.tfidf[kw_vector]
        tf_kw.sort(key= lambda x : x[1], reverse=True)
        result = [pair[0] for pair in tf_kw]

        return result

