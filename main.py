from fun import login, checkLogin, getInfo, getHot10
from strs import strings

if __name__ == '__main__':
    print(strings[0])
    if checkLogin():
        print(f'{getInfo("username")} {strings[4]}')
    else:
        print(strings[6])
        login()
    while True:
        s = input('>>> ')
        if s == 'exit':
            break
        if 'hot' in s:
            getHot10()
        if 'help' in s or '' == s:
            print('hot: get hot 10 news')
            print('exit: exit')
            print('help: help')