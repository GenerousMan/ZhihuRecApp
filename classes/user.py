from flask import jsonify

from classes.answer import Answer
from tools.io import read_user_topics, read_user_interactions


class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.topic_list = read_user_topics(self.user_id)
        # 这里记录了所有交互操作，仅是读出，还未处理
        self.interaction_all = read_user_interactions(self.user_id)

        # 处理每一个交互，并放入列表排序
        self.interaction_answer_list = self.process_interactions(self.interaction_all)

    def process_interactions(self, interaction_all):
        interaction_answers = interaction_all.split(",")
        answer_list = []
        for i, answer_item in enumerate(interaction_answers):
            # 分割为三部分
            answer_id, show_time, read_time = answer_item.split("|")
            print("Processing: ", answer_id)
            answer_object = Answer(answer_id)
            answer_object.answer_show_time = int(show_time)
            answer_object.answer_read_time = int(read_time)
            answer_object.print_self()
            answer_object = answer_object.export_self_to_dict()
            answer_list.append(answer_object)
            print("----------------------")
        answer_list.sort(key=lambda x: x["answer_show_time"])
        return answer_list

    def print_self(self):
        print("User_id:", self.user_id)
        print("Focus_topic_list", self.topic_list)
        print("Interaction_log", self.interaction_all)
        print("---------------Each Answer's info------------")
        for answer in self.interaction_answer_list:
            answer.print_self()
            print("-------------------")

    def export_self_to_dict(self):
        return {"user_ID": self.user_id, "user_bound_topics": self.topic_list,  "interaction_answers": self.interaction_answer_list}


if __name__ == "__main__":
    user_test = User("00d0148e0e24e48fbd863adc10c47965")
    user_test.print_self()
