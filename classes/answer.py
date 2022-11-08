import os
from tools.io import read_answer_bound_question_id, read_answer_bound_question_text, read_answer_text, read_answer_boundTopicIDs

class Answer:
    def __init__(self, answer_id):
        self.answer_id = answer_id

        # 这两个属性需要后续从100M里读取进来，留空
        self.answer_show_time = None
        self.answer_read_time = None

        # 这些可以直接从infos里读取得到
        self.answer_text = read_answer_text(self.answer_id)
        self.answer_topics = read_answer_boundTopicIDs(self.answer_id)
        self.question_id = read_answer_bound_question_id(self.answer_id)
        self.question_text = read_answer_bound_question_text(self.answer_id)
    def print_self(self):
        print("Answer_id:",self.answer_id)
        print("Answer_text:",self.answer_text)
        print("Answer_bound_topics:",self.answer_topics)
        print("Question_id:",self.question_id)
        print("Question_text:",self.question_text)

if __name__ == "__main__":
    test_answer = Answer("A21632993")
    print(test_answer.answer_id)
    print(test_answer.answer_text)
    print(test_answer.answer_topics)
    print(test_answer.question_id)
    print(test_answer.question_text)