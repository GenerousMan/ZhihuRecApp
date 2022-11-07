# coding=utf-8
# hello world
import json
from flask import Flask
from flask import request
from flask_cors import *
import flask

from tools.io import read_answer_text
from tools.io import read_answer_boundTopicIDs
from tools.tfidf import TFIDFSimilarity

#创建应用程序
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

model_path = "./model/"
tf_simi = TFIDFSimilarity()
tf_simi.load_tfidf(model_path)


@app.route("/fetch_answer_text", methods=['POST'])
def fetch_answer_text():
    # 输入answer_ID,（单个回答的字符串或者数组）, 检索得到答案文本数组
    answer_id = request.get_json().get('answer_ID')
    text = read_answer_text(answer_id)
    return text

@app.route("/fetch_answer_boundTopicIDs", methods=['POST'])
def fetch_answer_boundTopicIDs():
    # 输入answer_ID,获取指定answer id绑定的话题ID列表数组
    answer_id = request.get_json().get('answer_ID')
    text = read_answer_boundTopicIDs(answer_id)
    return text

@app.route("/compare_id", methods=['POST'])
@cross_origin()
def compare_id():
    # 输入两个answer_ID,获取两个回答的文本相似度
    answer_id_a = request.get_json().get('ID_a')
    answer_id_b = request.get_json().get('ID_b')
    text_a = read_answer_text(answer_id_a)
    text_b = read_answer_text(answer_id_b)
    simi = tf_simi.compare_similarity(text_a, text_b, 0.33)

    return str(simi)

@app.route("/compare_text", methods=['POST'])
@cross_origin()
def compare_text():
    # 输入两个文本,获取相似度
    text_a = request.get_json().get('text_a')
    text_b = request.get_json().get('text_b')
    simi = tf_simi.compare_similarity(text_a, text_b, 0.33)

    return str(simi)

@app.route("/get_text_characteristic_value", methods=['POST'])
@cross_origin()
def get_text_characteristic_value():
    # 输入原始文本，返回经tfidf处理后按照特征值由高到低排序的列表数组（去重）
    original_text = request.get_json().get('text')
    result = tf_simi.text_2_tfidf_characteristic_value(original_text)

    return result

@app.route("/fetch_user_interaction_answers", methods=['POST'])
@cross_origin()
def fetch_user_info_with_answers():
    # 输入用户的ID，返回该用户的基础信息以及该与用户交互的回答信息
    user_id = request.get_json().get('user_ID')
    return 'abcd'

if __name__ == "__main__":
    app.run(port=5050, debug=True)    #启动应用程序
