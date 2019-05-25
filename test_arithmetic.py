import unittest

import login
import generator


class TestLogin(unittest.TestCase):
    """test login and register"""

    def test_login(self):
        """登录测试"""
        self.assertEqual('登录失败，用户名或密码不能为空', login.login('', '', '学生'))
        self.assertEqual('用户名密码错误', login.login('test', 'test', '老师'))
        self.assertEqual(None, login.login('a', 'a', '学生'))

    def test_register(self):
        """注册测试"""
        self.assertEqual('注册失败，用户名或密码不能为空', login.registered('', '', '', '学生'))
        self.assertEqual('注册失败，两次输入密码不一致', login.registered('test', 'test', 'test2', '学生'))
        self.assertEqual('注册失败，用户名已存在', login.registered('a', 'a', 'a', '学生'))

    def test_get_pwd(self):
        """找回密码测试"""
        self.assertEqual({'identity': '老师', 'password': 'b'}, login.get_passwd('b', '老师'))
        self.assertEqual(None, login.get_passwd('b', '学生'))


class TestGenerator(unittest.TestCase):
    """test generator"""

    def test_question_list_generator(self):
        """生成题目测试"""
        self.assertEqual('运算范围应是一个整数', generator.generator_question('', [], ''))
        self.assertEqual('运算范围不能小于5', generator.generator_question('0', [], ''))
        self.assertEqual('需要至少一个运算符', generator.generator_question('5', ['( )'], ''))
        self.assertEqual('题目数量应是一个数字', generator.generator_question('5', ['+', '( )'], ''))
        self.assertIsInstance(generator.generator_question('5', ['+', '-', '*', '/', '( )'], '20'), list)

    def test_a_question_generator(self):
        """生成一道题目，判断测试"""
        question, ret = generator.make_a_question(66, ['+', '-', '*', '/'], 6, True)
        result = generator.check_question([(question, ret)], [ret])
        self.assertEqual(result, [True])


if __name__ == '__main__':
    unittest.main()
