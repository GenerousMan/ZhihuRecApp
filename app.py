# coding=utf-8
# hello world
from flask import Flask
from flask import request
import flask

from tools.io import read_answer
from tools.tfidf import TFIDFSimilarity

#创建应用程序
app = Flask(__name__)
model_path = "./model/"
tf_simi = TFIDFSimilarity()
tf_simi.load_tfidf(model_path)

# 写一个函数来处理浏览器发送过来的请求
@app.route("/")     #当访问网址时，默认执行下面函数
def index():
    return 'weclome to flask!!!'

@app.route("/fetch_answer", methods=['GET'])
def fetch_answer():
    # 获取指定answer id的文本信息
    answer_id = request.args.get('answer_id')
    print(answer_id)
    text = read_answer(answer_id)
    print(text)
    return text

@app.route("/compare_id", methods=['GET'])
def compare_id():
    # 获取指定answer id的文本信息
    answer_id_a = request.args.get('id_a')
    answer_id_b = request.args.get('id_b')
    print(answer_id_a,answer_id_b)
    text_a = read_answer(answer_id_a)
    text_b = read_answer(answer_id_b)
    simi = tf_simi.compare_similarity(text_a, text_b, 0.3)

    return str(simi)

@app.route("/compare_text", methods=['GET'])
def compare_text():
    # 获取指定answer id的文本信息
    text_a = request.args.get('text_a')
    text_b = request.args.get('text_b')
    simi = tf_simi.compare_similarity(text_a, text_b, 0.3)

    return str(simi)

@app.route("/roc")     #路由功能
def index1():
    #这里处理业务逻辑
    return '欢迎你!!!'

@app.route("/roc/qq")
def index2():
    #这里处理业务逻辑
    return 'hahaha!!!'

if __name__ == "__main__":
    app.run()    #启动应用程序
