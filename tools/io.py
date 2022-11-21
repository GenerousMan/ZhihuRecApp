import pandas as pd
import os
import numpy as np

answer_path = "source/answer_csv/"
user_path = "source/user_csv/"
interaction_path = "source/interaction_csv/"
question_path = "source/question_csv/"


def convert_question_csv(txt_path, csv_path, block_max):
    text_block = []
    block_count = 0
    fileHandler = open(txt_path, encoding='utf-8')
    ans_lines = fileHandler.readlines()
    print(len(ans_lines))
    ans_lines = [line.strip().split('\t') for line in ans_lines]
    ans_lines.sort(key=lambda x: int(x[0].split("Q")[-1]))
    # print(ans_lines)
    count_all = 0
    for i in range(len(ans_lines)):
        line = ans_lines[i]
        text_block.append(line)
        if (len(text_block) >= block_max):
            print(str(block_count) + " block saved.")
            df = pd.DataFrame(text_block)
            min_index = text_block[0][0].split("Q")[-1]
            df.to_csv(csv_path + min_index + ".csv", index=False)
            block_count += 1
            text_block = []

    fileHandler.close()


def convert_answer_csv(txt_path, csv_path, block_max):
    text_block = []
    block_count = 0
    fileHandler = open(txt_path, encoding='utf-8')
    ans_lines = fileHandler.readlines()
    print(len(ans_lines))
    ans_lines = [line.strip().split('\t') for line in ans_lines]
    ans_lines.sort(key=lambda x: int(x[0].split("A")[-1]))
    # print(ans_lines)
    count_all = 0
    for i in range(len(ans_lines)):
        line = ans_lines[i]
        text_block.append(line)
        if (len(text_block) >= block_max):
            print(str(block_count) + " block saved.")
            df = pd.DataFrame(text_block)
            min_index = text_block[0][0].split("A")[-1]
            df.to_csv(csv_path + min_index + ".csv", index=False)
            block_count += 1
            text_block = []

    fileHandler.close()


def convert_user_csv(txt_path, csv_path, block_max):
    text_block = []
    block_count = 0
    fileHandler = open(txt_path, encoding='utf-8')
    ans_lines = fileHandler.readlines()
    # print(len(ans_lines))
    ans_lines = [line.strip().split('\t') for line in ans_lines]
    ans_lines.sort(key=lambda x: x[0])
    # print(ans_lines)

    count_all = 0
    for i in range(len(ans_lines)):
        line = ans_lines[i]
        text_block.append(line)
        if (len(text_block) >= block_max):
            print(str(block_count) + " block saved.")
            df = pd.DataFrame(text_block)
            min_index = text_block[0][0]
            print(min_index)
            df.to_csv(csv_path + min_index + ".csv", index=False)
            block_count += 1
            text_block = []

    fileHandler.close()


def convert_interaction_csv(txt_path, csv_path, block_max):
    text_block = []
    block_count = 0
    fileHandler = open(txt_path, encoding='utf-8')
    # print(ans_lines)
    ans_lines = fileHandler.readlines()
    # print(len(ans_lines))
    ans_lines = [line.strip().split('\t') for line in ans_lines]
    ans_lines.sort(key=lambda x: x[0])
    # print(ans_lines)
    count_all = 0
    for i in range(len(ans_lines)):
        line = ans_lines[i]
        if (line == None):
            break
        text_block.append(line)
        if (len(text_block) >= block_max):
            print(str(block_count) + " block saved.")
            df = pd.DataFrame(text_block)
            min_index = text_block[0][0]
            print(min_index)
            df.to_csv(csv_path + min_index + ".csv", index=False)
            block_count += 1
            text_block = []

    fileHandler.close()


def read_answer_text(answer_id):
    # 输入answer id（单个回答的字符串或者数组）, 检索得到答案文本数组
    # 如果answer id是一个字符串，则也返回一个字符串；如果answer id 是多个字符串组成的数组，则也返回对应的多字符串数组
    file_list = os.listdir(answer_path)
    file_list.sort(key=lambda k: int(k.split(".")[0]))

    answer_nums = []
    if (type(answer_id) == type('string')):
        answer_nums = [int(answer_id.split("A")[-1])]
        result = ''
    if (type(answer_id) == type([])):
        answer_nums = [int(answer_ID.split("A")[-1]) for answer_ID in answer_id]
        result = []

    for answer_num in answer_nums:
        index_file = ""
        for i in range(len(file_list)):
            this_start = int(file_list[i].split(".")[0])
            if (this_start <= answer_num):
                if (i == len(file_list) - 1 or int(file_list[i + 1].split(".")[0]) > answer_num):
                    index_file = file_list[i]
                    df = pd.read_csv(answer_path + index_file)
                    # 找到分块文件中对应的answer_num数据行
                    if (len(df[df['0'] == "A" + str(answer_num)].index.tolist()) == 0):
                        # 找不到对应数据
                        return ''
                    line_index = df[df['0'] == "A" + str(answer_num)].index.tolist()[0]
                    # print("The answer "+answer_num+ " is in file "+index_file+"'s "+str(line_index)+" line.")
                    # 输出索引第16列（回答的文本信息）
                    if (type(answer_id) == type('string')):
                        result = df['16'][line_index]
                    if (type(answer_id) == type([])):
                        result.append(df['16'][line_index])

    return result


def read_user_topics(user_id):
    # 输入user id, 检索得到用户绑定的话题列表
    file_list = os.listdir(user_path)
    file_list.sort(key=lambda k: k.split("."))

    result = []

    for i in range(len(file_list)):
        this_start = file_list[i].split(".")[0]
        if (this_start <= user_id):
            if (i == len(file_list) - 1 or file_list[i + 1].split(".")[0] > user_id):
                index_file = file_list[i]
                df = pd.read_csv(user_path + index_file)
                if (len(df[df['0'] == user_id].index.tolist()) == 0):
                    # 找不到对应数据
                    return []
                line_index = df[df['0'] == user_id].index.tolist()[0]
                return df['26'][line_index].split(",") if type(df['26'][line_index]) == type('string') else []
    return []


def read_answer_boundTopicIDs(answer_id):
    # 输入answer id，检索得到该回答绑定的话题ID列表数组
    answer_num = int(answer_id.split("A")[-1])
    file_list = os.listdir(answer_path)
    file_list.sort(key=lambda k: int(k.split(".")[0]))
    # print(file_list)
    index_file = ""
    for i in range(len(file_list)):
        this_start = int(file_list[i].split(".")[0])
        if (this_start <= answer_num):
            if (i == len(file_list) - 1 or int(file_list[i + 1].split(".")[0]) > answer_num):
                index_file = file_list[i]

    # print(index_file)
    df = pd.read_csv(answer_path + index_file)
    # 找到分块文件中对应的answer_id数据行
    if (len(df[df['0'] == answer_id].index.tolist()) == 0):
        # 找不到对应数据
        return []

    line_index = df[df['0'] == answer_id].index.tolist()[0]
    # 输出索引第17列（回答绑定的话题IDs，半角逗号分割）
    if (pd.isna(df['17'][line_index])):
        # topic列表为空的情况
        return []
    return df['17'][line_index].split(",")


def read_user_interactions(user_id):
    file_list = os.listdir(interaction_path)
    file_list.sort(key=lambda k: k.split("."))

    for i in range(len(file_list)):
        this_start = file_list[i].split(".")[0]
        if (this_start <= user_id):
            if (i == len(file_list) - 1 or file_list[i + 1].split(".")[0] > user_id):
                index_file = file_list[i]
                df = pd.read_csv(interaction_path + index_file)
                if (len(df[df['0'] == user_id].index.tolist()) == 0):
                    # 找不到对应数据
                    return ''
                line_index = df[df['0'] == user_id].index.tolist()[0]
                return df['2'][line_index] if type(df['2'][line_index]) == type('string') else ''


def read_answer_bound_question_id(answer_id):
    answer_num = int(answer_id.split("A")[-1])
    file_list = os.listdir(answer_path)
    file_list.sort(key=lambda k: int(k.split(".")[0]))
    # print(file_list)
    index_file = ""
    for i in range(len(file_list)):
        this_start = int(file_list[i].split(".")[0])
        if (this_start <= answer_num):
            if (i == len(file_list) - 1 or int(file_list[i + 1].split(".")[0]) > answer_num):
                index_file = file_list[i]

    # print(index_file)
    df = pd.read_csv(answer_path + index_file)
    # 找到分块文件中对应的answer_id数据行
    if (len(df[df['0'] == answer_id].index.tolist()) == 0):
        # 找不到对应数据
        return ""

    line_index = df[df['0'] == answer_id].index.tolist()[0]
    # 输出索引第1列,即问题id
    question_id = df['1'][line_index]
    if (pd.isna(question_id)):
        return ""
    else:
        return df['1'][line_index]


def read_answer_bound_question_text(answer_id):
    # 先找到问题id
    question_id = read_answer_bound_question_id(answer_id)

    if (question_id == ""):
        # 这个回答绑定的问题是空的
        return ""

    question_num = int(question_id.split("Q")[-1])
    file_list = os.listdir(question_path)
    file_list.sort(key=lambda k: int(k.split(".")[0]))
    index_file = ""
    for i in range(len(file_list)):
        this_start = int(file_list[i].split(".")[0])
        if (this_start <= question_num):
            if (i == len(file_list) - 1 or int(file_list[i + 1].split(".")[0]) > question_num):
                index_file = file_list[i]
    # print(index_file)
    df = pd.read_csv(question_path + index_file)
    # 找到分块文件中对应的answer_id数据行
    if (len(df[df['0'] == question_id].index.tolist()) == 0):
        # 找不到对应数据
        return ''

    line_index = df[df['0'] == question_id].index.tolist()[0]
    # 输出索引第6列，即问题text
    return df['6'][line_index]


if __name__ == "__main__":
    convert_answer_csv("zhihuRec/answer_infos.txt", "source/answer_csv/", 1000)
    convert_user_csv("zhihuRec/user_infos.txt", "source/user_csv/", 1000)
    convert_interaction_csv("zhihuRec/zhihu100M.txt", "source/interaction_csv/", 1000)
    convert_question_csv("zhihuRec/question_infos.txt", "source/question_csv/", 1000)

    # print(read_user_topics("0049cc47ffba086c35bce638f38b97d5"))
    # print(read_answer_text("A21632993"))
    # print(read_user_interactions("908ec3ef94c640c15e565720a1e4030f"))
    print(read_answer_bound_question_id("A21632993"))
    print(read_answer_bound_question_text("A21632993"))
