import json


def GetAnswerPara():
    # 解析Json文件,需要手动修改该Json文件内容以答不同的试卷.
    with open("answer_json/answer.json", encoding='utf-8') as f:
        content = json.load(f)
    # 取题目数量
    content_keys = content.keys()
    for key in content_keys:
        key_num = key
    print("题目数量", key_num)
    # 取题目列表
    question_list = content[key_num]
    # 定义结果para
    para = ""
    # 遍历题目列表: 1,取testTestid 2,取testKey 3,形成一个答案参数 4,添加到para
    for question in question_list:
        # print(question)
        testTestid = question['testTestid']
        testKey = question['testKey']
        question_para = str(testTestid) + '-' + testKey + '@'
        para += question_para
    print(para)

if __name__ == '__main__':
    GetAnswerPara()