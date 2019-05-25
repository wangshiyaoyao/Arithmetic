"""注册登录与密码找回"""


def read_user_info():
    """读取用户信息"""
    user_info_file = open('users.txt', 'a+', encoding='utf-8')
    user_info_file.seek(0)
    try:
        user_info = eval(user_info_file.read())
    except SyntaxError:
        user_info = {}
    user_info_file.close()
    return user_info


USER_INFO = read_user_info()


def registered(uname, pwd, pwd2, identity):
    """注册函数"""
    if not uname or not pwd or not pwd2:
        return "注册失败，用户名或密码不能为空"
    if pwd != pwd2:
        return "注册失败，两次输入密码不一致"
    if uname in USER_INFO:
        return "注册失败，用户名已存在"
    USER_INFO[uname] = {'password': pwd, 'identity': identity}
    user_file = open('users.txt', 'w', encoding='utf-8')
    user_file.write(str(USER_INFO))
    user_file.close()
    return None


def login(uname, pwd, identity):
    """登录函数"""
    if not uname or not pwd:
        return "登录失败，用户名或密码不能为空"
    if uname in USER_INFO and USER_INFO[uname]['password'] == pwd \
            and USER_INFO[uname]['identity'] == identity:
        return None
    return '用户名密码错误'


def get_passwd(uname, identity):
    """找回密码"""
    if uname in USER_INFO and USER_INFO[uname]['identity'] == identity:
        return USER_INFO[uname]
    return None
