from fun import login, checkLogin, getInfo
from strs import strings

if __name__ == '__main__':
    print(strings[0])
    if checkLogin():
        print(f'{getInfo("username")} {strings[4]}')
    else:
        print(strings[6])
        login()
        if checkLogin():
            pass
        else:
            print(strings[5])