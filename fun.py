import hashlib
import requests
import time
import json
import getpass
from strs import strings

urlBase = 'https://bbs.uestc.edu.cn/mobcent/app/web/index.php'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
}
infoFile = 'info.json'



def getInfo(key: str):
    try:
        info = json.load(open(infoFile, 'r', encoding = 'utf-8'))
        return info[key]
    except:
        return ''

def setInfo(key: str, value):
    try:
        info = json.load(open(infoFile, 'r', encoding = 'utf-8'))
    except:
        info = {}
    info[key] = value
    json.dump(info, open(infoFile, 'w', encoding = 'utf-8'))

def getAppHashValue() -> str:
    s = f'{time.time()}'[:5] + 'appbyme_key'
    apphash = hashlib.md5(s.encode('utf-8')).hexdigest()
    return apphash[8:16]

def checkLogin() -> bool:
    if getInfo('token') == '' or getInfo('secret') == '' or getInfo('username') == '' or getInfo('password') == '':
        return False
    paramst = {
        'r': 'forum/postlist',
        'topicId': 1000,
        'pageSize': 1,
        'page': 1,
        'order': 0,
        'apphash': '',
        'accessToken': getInfo('token'),
        'accessSecret': getInfo('secret')
    }
    res = requests.post(urlBase, params = paramst, headers = headers)
    # print(res.json())
    if res.json()['rs'] == 1:
        return True
    else:
        return False

def loginWithUsernamePassword(username: str = '', password: str = ''):
    paramsLogin = {
        'r': 'user/login',
        'type': 'login',
        'username': username,
        'password': password,
    }
    try:
        res = requests.post(urlBase, params = paramsLogin, headers = headers)
        # print(res.json())
        if res.json()['rs'] != 1:
            print(res.json()['errcode'])
            return
        info = res.json()
        setInfo('token', info['token'])
        setInfo('secret', info['secret'])
        setInfo('username', username)
        setInfo('password', password)
        print(f"{info['userName']}({info['userTitle']}) {strings[3]} {info['creditShowList'][0]['title']}: {info['creditShowList'][0]['data']}, {info['creditShowList'][1]['title']}: {info['creditShowList'][1]['data']}")
    except Exception as e:
        print(e)

def login(username: str = '', password: str = ''):
    if username != '' and password != '':
        loginWithUsernamePassword(username, password)
    else:
        un = input(strings[1])
        pw = getpass.getpass(strings[2])
        loginWithUsernamePassword(un, pw)