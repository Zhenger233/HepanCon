from fun import getAppHashValue, login, getInfo, setInfo, checkLogin, getHot10
from strs import strings

myUsername = getInfo('username')
myPassword = getInfo('password')

def testLogin():
    print(getAppHashValue())
    print(getInfo('token'))
    setInfo('token', '123456')
    login(myUsername, myPassword)
    print(getInfo('token'))
    print(getInfo('secret'))
    checkLogin()

def testHot10():
    getHot10()

def testStrings():
    print(strings)

if __name__ == '__main__':
    testHot10()