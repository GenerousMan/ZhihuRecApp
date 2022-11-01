import pandas as pd
import os

import tools.tfidf
import tools.io

if __name__ == "__main__":
    # 计算全部文档的tf-idf
    txt_path = "zhihuRec/"
    fileHandler = open(txt_path)
    while True:
        line = fileHandler.readline()
        if not line:
            break
        line = line.strip().split('\t')