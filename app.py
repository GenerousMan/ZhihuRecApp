# coding=utf-8
# hello world
import json
from flask import Flask
from flask import request
from flask_cors import *
import flask

from tools.io import read_answer
from tools.tfidf import TFIDFSimilarity

#创建应用程序
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

model_path = "./model/"
tf_simi = TFIDFSimilarity()
tf_simi.load_tfidf(model_path)

# 写一个函数来处理浏览器发送过来的请求
@app.route("/test", methods=['POST'])     #当访问网址时，默认执行下面函数
def index():
    return 'weclome to flask!!!'

@app.route("/fetch_answer", methods=['POST'])
def fetch_answer():
    # 输入answer_ID,获取指定answer id的文本信息
    answer_id = request.get_json().get('answer_ID')
    text = read_answer(answer_id)
    print(text)
    return text

@app.route("/compare_id", methods=['POST'])
@cross_origin()
def compare_id():
    # 输入两个answer_ID,获取两个回答的文本相似度
    answer_id_a = request.get_json().get('ID_a')
    answer_id_b = request.get_json().get('ID_b')
    text_a = read_answer(answer_id_a)
    text_b = read_answer(answer_id_b)
    simi = tf_simi.compare_similarity(text_a, text_b, 0.3)

    return json.dumps(simi)
    #return text_b

@app.route("/compare_text", methods=['POST'])
@cross_origin()
def compare_text():
    # 输入两个文本,获取相似度
    text_a = request.get_json().get('text_a')
    text_b = request.get_json().get('text_b')
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
    app.run(port=5050, debug=True)    #启动应用程序
