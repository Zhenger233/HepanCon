strSelect = 1
strSet = {
    0: ['Welcome to HepanCon!', '欢迎使用 HepanCon！'],
    1: ['Please input your Username:', '请输入用户名：'],
    2: ['Please input your Password:', '请输入密码：'],
    3: ['Login Success!', '登录成功！'],
    4: ['Have logged in!', '已经登录!'],
    5: ['Login Failed!', '登录失败！'],
    6: ['Please login!', '请登录！'],
}
strings = { k: strSet[k][strSelect] for k in strSet }