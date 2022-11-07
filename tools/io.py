import pandas as pd
import os
answer_path = "source/answer_csv/"

def convert_csv(txt_path, csv_path, block_max):
    text_block = []
    block_count = 0
    fileHandler = open(txt_path)
    ans_lines = fileHandler.readlines()
    print(len(ans_lines))
    ans_lines = [ line.strip().split('\t') for line in ans_lines]
    ans_lines.sort(key=lambda x:int(x[0].split("A")[-1]))
    # print(ans_lines)
    count_all = 0
    for i in range(len(ans_lines)):
        line = ans_lines[i]
        text_block.append(line)
        if(len(text_block)>=block_max):
            print(str(block_count)+" block saved.")
            df = pd.DataFrame(text_block)
            min_index = text_block[0][0].split("A")[-1]
            df.to_csv(csv_path+min_index+".csv", index=False)
            block_count += 1
            text_block = []

    fileHandler.close()


def read_answer_text(answer_id):
    # 输入answer id（单个回答的字符串或者数组）, 检索得到答案文本数组
    answer_nums = []
    if ( type(answer_id) == type('string')):
        answer_nums = [int(answer_id.split("A")[-1])]
    if (type(answer_id) == type([])):
        answer_nums = [int(answer_ID.split("A")[-1]) for answer_ID in answer_id]

    file_list = os.listdir(answer_path)
    file_list.sort(key = lambda k:int(k.split(".")[0]))

    result = []

    for answer_num in answer_nums:
        index_file = ""
        for i in range(len(file_list)):
            this_start = int(file_list[i].split(".")[0])
            if(this_start <= answer_num):
                if(i == len(file_list)-1 or int(file_list[i+1].split(".")[0])>answer_num):
                    index_file = file_list[i]
                    df = pd.read_csv(answer_path+index_file)
                    #找到分块文件中对应的answer_num数据行
                    line_index = df[df['0'] == "A"+str(answer_num)].index.tolist()[0]
                    #print("The answer "+answer_num+ " is in file "+index_file+"'s "+str(line_index)+" line.")
                    #输出索引第16列（回答的文本信息）
                    result.append(df['16'][line_index])

    return result

def read_answer_boundTopicIDs(answer_id):
    # TODO：如果对应数据行绑定的话题ID为空，如何处理？
    # 输入answer id，检索得到该回答绑定的话题ID列表数组
    answer_num = int(answer_id.split("A")[-1])
    file_list = os.listdir(answer_path)
    file_list.sort(key = lambda k:int(k.split(".")[0]))
    print(file_list)
    index_file = ""
    for i in range(len(file_list)):
        this_start = int(file_list[i].split(".")[0])
        if(this_start <= answer_num):
            if(i == len(file_list)-1 or int(file_list[i+1].split(".")[0])>answer_num):
                index_file = file_list[i]

    print(index_file)
    df = pd.read_csv(answer_path+index_file)
    #找到分块文件中对应的answer_id数据行
    line_index = df[df['0'] == answer_id].index.tolist()[0]
     #输出索引第17列（回答绑定的话题IDs，半角逗号分割）
    return df['17'][line_index].split(",")

if __name__ == "__main__":
    convert_csv("zhihuRec/answer_infos.txt","source/answer_csv/",10000)
    read_answer_text("A21632993")