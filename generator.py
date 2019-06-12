"""试卷生成"""
import random
import re


def make_a_question(operation_range, opeartions, nums, brackets):
    """生成一道题目"""
    def uncheck_question():
        question = []
        for _ in range(nums):
            num = random.randint(-operation_range, operation_range)
            oper = random.choice(opeartions)
            if num < 0:
                question.append('(' + str(num) + ')')
            else:
                question.append(str(num))
            question.append(oper)
        # 去掉最后的符号
        del question[-1]

        # 添加括号
        if brackets:
            index = []
            while True:
                index = random.sample(range(nums), 2)
                index.sort()
                if index != [0, nums-1]:
                    break
            question.insert(index[1] * 2 + 1, ')')
            question.insert(index[0] * 2, '(')

        return ''.join(question)

    ret = None
    while True:
        a_question = uncheck_question()
        try:
            ret = eval(a_question)
            if int(ret) != ret:
                continue
        except ZeroDivisionError:
            continue
        break
    return a_question, ret


def generator_question(operation_range, opeartions, number):
    """题目生成函数"""
    brackets = False
    if '( )' in opeartions:
        brackets = True
        opeartions.remove('( )')

    # 参数检查
    try:
        operation_range = int(operation_range)
    except ValueError:
        return '运算范围应是一个整数'
    if operation_range < 5:
        return '运算范围不能小于5'
    if not opeartions:
        return '需要至少一个运算符'
    try:
        number = int(number)
    except ValueError:
        return '题目数量应是一个数字'
    nums = 6    # 一道题目中数字个数

    question_list = []
    for _ in range(number):
        question, ret = make_a_question(operation_range, opeartions, nums, brackets)
        question_list.append((question, ret))

    return question_list


def check_question(question_list, q_result):
    """批改题目"""
    number = len(question_list)
    result = [False] * number
    pattern = re.compile(r'^[-\+*/ \.\d\(\)]+$')
    for index in range(number):
        ret = pattern.match(q_result[index])
        if ret is not None:
            try:
                ret = eval(ret.group())
            except ZeroDivisionError:
                pass
            if ret == question_list[index][1]:
                result[index] = True
    return result
