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


def read_answer(answer_id):
    # 输入answer id, 检索得到答案文本
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
    print(df[df['0'] == answer_id].index.tolist())
    ans_list = df[df['0'] == answer_id].index.tolist()
    if (len(ans_list)==0):
        return None

    line_index = ans_list[0]
    print("The answer "+answer_id+ " is in file "+index_file+"'s "+str(line_index)+" line.")

    print(df['16'][line_index])
    return df['16'][line_index]

if __name__ == "__main__":
    convert_csv("zhihuRec/answer_infos.txt","source/answer_csv/",10000)
    read_answer("A21632993")