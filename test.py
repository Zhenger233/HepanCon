from fun import getAppHashValue, login, getInfo, setInfo, checkLogin
from strs import strings

myUsername = getInfo('username')
myPassword = getInfo('password')

def test():
    print(getAppHashValue())
    print(getInfo('token'))
    setInfo('token', '123456')
    login(myUsername, myPassword)
    print(getInfo('token'))
    print(getInfo('secret'))
    checkLogin()
    

if __name__ == '__main__':
    print(strings)