"""前端界面代码,程序入口"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog

import login
import generator

G_IDENTITY = '学生'


def init_win(window, title, size='300x100'):
    """初始化窗口"""
    # 清空界面控件
    for widget in window.winfo_children():
        widget.destroy()
    # 标题
    window.title(title)
    # 窗口大小
    window.geometry(size)


def win_login(window):
    """登录界面"""
    init_win(window, '四则运算')
    # 窗口不可改变
    window.resizable(False, False)

    # user information
    lab_user_name = tk.Label(window, text='用户名: ')
    user_name = tk.Entry(window)
    lab_user_name.grid(row=0, column=0)
    user_name.grid(row=0, column=1)

    lab_usr_pwd = tk.Label(window, text='密码: ')
    usr_pwd = tk.Entry(window, show='*')
    lab_usr_pwd.grid(row=1, column=0)
    usr_pwd.grid(row=1, column=1)

    identity_lab = tk.Label(window, text='身份: ')
    identity = ttk.Combobox(window, values=('学生', '老师'), state='readonly', width=18)
    identity.current(0)
    identity_lab.grid(row=2, column=0)
    identity.grid(row=2, column=1)

    def usr_login():
        """登录进入题目工厂界面"""
        ret = login.login(user_name.get(), usr_pwd.get(), identity.get())
        if ret:
            messagebox.showwarning('登录失败', ret)
        else:
            # 进入题目工厂界面
            global G_IDENTITY
            G_IDENTITY = identity.get()
            win_factory_exam_question(window)

    def usr_sign_up():
        # 进入注册界面
        win_sign_up(window)

    def usr_forget_pwd():
        # 进入忘记密码界面
        win_forget_pwd(window)

    # login and sign up button
    btn_login = tk.Button(window, text='登录', command=usr_login)
    btn_login.grid(row=3, column=0)
    btn_sign_up = tk.Button(window, text='注册', command=usr_sign_up)
    btn_sign_up.grid(row=3, column=1)
    btn_forget_pwd = tk.Button(window, text='忘记密码', command=usr_forget_pwd)
    btn_forget_pwd.grid(row=3, column=2)


def win_sign_up(window):
    """注册界面"""
    init_win(window, '注册')

    lab_user_name = tk.Label(window, text='用户名: ')
    user_name = tk.Entry(window)
    lab_user_name.grid(row=0, column=0)
    user_name.grid(row=0, column=1)

    lab_usr_pwd = tk.Label(window, text='密码: ')
    usr_pwd = tk.Entry(window, show='*')
    lab_usr_pwd.grid(row=1, column=0)
    usr_pwd.grid(row=1, column=1)

    lab_usr_pwd2 = tk.Label(window, text='重复密码: ')
    usr_pwd2 = tk.Entry(window, show='*')
    lab_usr_pwd2.grid(row=2, column=0)
    usr_pwd2.grid(row=2, column=1)

    identity_lab = tk.Label(window, text='身份: ')
    identity = ttk.Combobox(window, values=('学生', '老师'), state='readonly', width=18)
    # default:学生
    identity.current(0)
    identity_lab.grid(row=3, column=0)
    identity.grid(row=3, column=1)

    def usr_sign_up():
        """用户注册"""
        ret = login.registered(user_name.get(), usr_pwd.get(), usr_pwd2.get(), identity.get())
        if ret:
            messagebox.showwarning('注册失败', ret)
        else:
            messagebox.showinfo('注册成功', '注册成功')

    def quit_to_win_login():
        """返回登录界面"""
        win_login(window)

    btn_sign_up = tk.Button(window, text='注册', command=usr_sign_up)
    btn_sign_up.grid(row=0, column=2, rowspan=2)
    btn_quit = tk.Button(window, text='返回', command=quit_to_win_login)
    btn_quit.grid(row=2, column=2, rowspan=2)


def win_forget_pwd(window):
    """找回密码界面"""
    init_win(window, '找回密码')

    # user information
    lab_user_name = tk.Label(window, text='用户名: ')
    user_name = tk.Entry(window)
    lab_user_name.grid(row=0, column=0)
    user_name.grid(row=0, column=1)

    identity_lab = tk.Label(window, text='身份: ')
    identity = ttk.Combobox(window, values=('学生', '老师'), state='readonly', width=18)
    identity.current(0)
    identity_lab.grid(row=2, column=0)
    identity.grid(row=2, column=1)

    def recover_pwd():
        """找回密码"""
        ret = login.get_passwd(user_name.get(), identity.get())
        if ret:
            messagebox.showinfo('找回密码', ret)
        else:
            messagebox.showwarning('找回失败', '密码找回失败')

    def quit_to_win_login():
        """返回登录界面"""
        win_login(window)

    btn_recover_pwd = tk.Button(window, text='找回', command=recover_pwd)
    btn_recover_pwd.grid(row=4, column=0)
    btn_quit = tk.Button(window, text='返回', command=quit_to_win_login)
    btn_quit.grid(row=4, column=1)


def win_factory_exam_question(window):
    """题目工厂界面"""
    init_win(window, '题目工厂')

    # check = window.register(check_int)
    lab_range = tk.Label(window, text='运算范围: ')
    operation_range = tk.Entry(window)
    lab_range.grid(row=0, column=0)
    operation_range.grid(row=0, column=1)

    # 符号复选框
    opeartions = {}
    frame = tk.Frame(window)
    frame.grid(row=1, columnspan=5)
    for each in ('+', '-', '*', '/', '( )'):
        status = tk.IntVar()
        operation = tk.Checkbutton(frame, text=each, variable=status)
        operation.pack(side='left')
        opeartions[each] = status

    lab_number = tk.Label(window, text='题目数量: ')
    number = ttk.Spinbox(window, from_=5, to=100, increment=5, state='readonly')
    lab_number.grid(row=2, column=0)
    number.grid(row=2, column=1)

    def generate_exam_question():
        """生成题目
        答题界面
        试卷预览界面"""

        # 取出选择的符号
        opers = []
        for key in opeartions:
            if opeartions[key].get():
                opers.append(key)
        # 生成题目列表
        question_list = generator.generator_question(operation_range.get(), opers, number.get())
        # 参数有问题,消息框提示
        if isinstance(question_list, str):
            messagebox.showwarning('提示', question_list)
            return

        if G_IDENTITY == '学生':
            win_exam(window, question_list)
        else:
            win_watch_result(window, question_list, print_exam)

    def quit_to_win_login():
        """返回登录界面"""
        win_login(window)

    btn_sign_up = tk.Button(window, text='生成题目', command=generate_exam_question)
    btn_sign_up.grid(row=0, column=5, rowspan=2)
    btn_quit = tk.Button(window, text='返回', command=quit_to_win_login)
    btn_quit.grid(row=2, column=5)


def print_exam(text_widget, content):
    """输出题目预览"""
    for question, ret in content:
        text_widget.insert("end", f'题目:{question}\n\t答案:{ret}\n')


def print_exam_result(text_widget, content):
    """输出考试结果"""
    for question, a_result, is_true in content:
        text_widget.insert("end", f'题目:{question[0]}\n'
                           f'\t正确答案:{question[1]}\t你的答案:{a_result}\t结果:{is_true}\n')


def win_watch_result(window, exam, fun_print):
    """预览题目界面"""
    init_win(window, '查看结果', '800x400')

    text = scrolledtext.ScrolledText(window)
    fun_print(text, exam)
    text.pack(fill='x')

    def save():
        try:
            fobj = filedialog.asksaveasfile()
            fobj.write(text.get(1.0, 'end'))
            fobj.close()
        except Exception:
            messagebox.showerror('警告', '保存失败')
        else:
            messagebox.showinfo('提示', '保存成功')

    def quit_to_win_login():
        """返回工厂界面"""
        win_factory_exam_question(window)

    btn_save = tk.Button(window, text='保存', command=save)
    btn_quit = tk.Button(window, text='返回', command=quit_to_win_login)
    btn_save.pack(side='left', expand=True)
    btn_quit.pack(side='left', expand=True)


def win_exam(window, question_list):
    """考试答题界面"""
    init_win(window, '考试')

    index = 1   # 题目序号
    question_num = len(question_list)
    result = [''] * question_num  # 存放作答
    text = tk.StringVar()
    question = tk.Label(window, textvariable=text)
    text.set(f'第{index}/{question_num}题:{question_list[index - 1][0]}')
    question_result = tk.StringVar()
    question_input = tk.Entry(window, textvariable=question_result)
    question.grid(row=0, column=0, columnspan=3)
    question_input.grid(row=1, column=0, columnspan=3)

    def previous_question():
        nonlocal index
        result[index-1] = question_result.get()
        index -= 1
        index = max(index, 1)
        text.set(f'第{index}/{question_num}题:{question_list[index - 1][0]}')
        question_result.set('')

    def next_question():
        nonlocal index
        result[index-1] = question_result.get()
        index += 1
        index = min(index, len(question_list))
        text.set(f'第{index}/{question_num}题:{question_list[index - 1][0]}')
        question_result.set('')

    def finish():
        result[index - 1] = question_result.get()
        # 计算分数
        review_result = generator.check_question(question_list, result)
        grade = review_result.count(True)/len(review_result) * 100
        ret = messagebox.askokcancel('成绩', f'分数:{grade}\n查看答案?')
        if ret:
            question_grade_result = list(zip(question_list, result, review_result))
            # 查看答案
            win_watch_result(window, question_grade_result, print_exam_result)
        else:
            # 返回题目工厂界面
            win_factory_exam_question(window)

    btn_prev = tk.Button(window, text='上一题', command=previous_question)
    btn_next = tk.Button(window, text='下一题', command=next_question)
    btn_finish = tk.Button(window, text='交卷', command=finish)
    btn_prev.grid(row=2, column=0)
    btn_next.grid(row=2, column=1)
    btn_finish.grid(row=2, column=2)


if __name__ == '__main__':
    WIN = tk.Tk()
    win_login(WIN)
    WIN.mainloop()
