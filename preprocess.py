import os
import time

from tools.tfidf import TFIDFSimilarity
import tools.io

if __name__ == "__main__":
    # 计算全部文档的tf-idf
    txt_path = "./zhihuRec/answer_infos.txt"

    # 将训练好的模型存入model文件夹中
    model_path = "./model/"
    fileHandler = open(txt_path)
    tf_simi = TFIDFSimilarity()
    count = 0
    answer_list = []

    start = time.clock()

    if(os.path.exists(model_path)):
        # 如果有保存好的模型，直接读取，否则将重新训练
        tf_simi.load_tfidf(model_path)
    else:
        os.mkdir(model_path)
        # 读取所有回答数据
        while True:
            line = fileHandler.readline()
            if not line:
                break
            line = line.strip().split('\t')
            answer = line[-2].split(" ")
            if (count % 10000 == 0):
                print(count)
            if (answer == ['0']):
                # 说明已被关闭
                continue
            answer_list.append(answer)
            count += 1
        # 对答案排序
        answer_list.sort(key=lambda x: len(x), reverse=True)
        # 输出排名前5000,10000的答案长度，因为太短的答案没价值，还会影响idf结果
        print(len(answer_list[0]), len(answer_list[5000]), len(answer_list[10000]), len(answer_list[20000]))
        print(len(answer_list))

        print("training...")

        tf_simi.train(answer_list[:200000])
        tf_simi.save_tfidf("./model/")

    end = time.clock()
    print("time cost:",end-start)

    # 三个测试，验证jaccard相似度的效果。

    # test 1: 完全无关文本
    tf_simi.compare_similarity(
        "24421 7113 17742 9411 313374 6252 397570 6343 10699 351192 258573 434589 10591 19855 334383 10591 614820 24083 240584 17742 246867 434589 10591",
        "6121 11765 11628 374050 17742 504345 239609 6252 270061 533705 17742 24421 7280 345607 6252 11628 12741 531299 660591 17742",
         0.3)
    # test 2: 强相关文本
    tf_simi.compare_similarity(
        "24421 7113 17742 9411 313374 6252 397570 6343 10699 351192 258573 434589 10591 19855 334383 10591 614820 24083 240584 17742 246867 434589 10591",
        "351192 258573 434589 10591 19855 334383 10591 614820 24083 240584 17742 246867 10591 11129 6252 369184 12741 842975 8201 24105 12741 220849",
        0.3)
    # test 3: 完全一致文本
    tf_simi.compare_similarity(
        "24421 7113 17742 9411 313374 6252 397570 6343 10699 351192 258573 434589 10591 19855 334383 10591 614820 24083 240584 17742 246867 434589 10591",
        "24421 7113 17742 9411 313374 6252 397570 6343 10699 351192 258573 434589 10591 19855 334383 10591 614820 24083 240584 17742 246867 434589 10591",
        0.3)