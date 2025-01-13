import hashlib
import requests
import time
import json
import getpass
from strs import strings
from pprint import pprint


urlBase = 'https://bbs.uestc.edu.cn/mobcent/app/web/index.php'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'Accept': 'application/json, text/plain, */*;'
}
infoFile = 'info.json'
urlBaseNew = 'https://bbs.uestc.edu.cn/star/api/v1'
session = requests.Session()

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
    authString = f'{time.time()}'[:5] + 'appbyme_key'
    apphash = hashlib.md5(authString.encode('utf-8')).hexdigest()
    return apphash[8:16]

def getReplyList(tid: int, page: int = 1, pageSize: int = 10):
    paramst = {
        'r': 'forum/postlist',
        'topicId': tid,
        'pageSize': pageSize,
        'page': page,
        'order': 0,
        'accessToken': getInfo('token'),
        'accessSecret': getInfo('secret')
    }
    res = requests.post(urlBase, params = paramst, headers = headers)
    if res.json()['rs'] == 1:
        return res.json()['list']
    else:
        print(res.json()['errcode'])
        return []

def checkLogin() -> bool:
    if getInfo('token') == '' or getInfo('secret') == '' or getInfo('username') == '' or getInfo('password') == '':
        return False
    paramst = {
        'r': 'forum/postlist',
        'topicId': 2203132,
        'pageSize': 1,
        'page': 1,
        'order': 1,
        'accessToken': getInfo('token'),
        'accessSecret': getInfo('secret')
    }
    res = requests.post(urlBase, params = paramst, headers = headers)
    pprint(res.json())
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
        print(strings[5])
        print(e)

def login(username: str = '', password: str = ''):
    if username != '' and password != '':
        loginWithUsernamePassword(username, password)
    else:
        un = input(strings[1])
        pw = getpass.getpass(strings[2])
        loginWithUsernamePassword(un, pw)

def getNewAuth():
    resp = session.post(urlBase, params={
        'r': 'user/login',
        'type': 'login',
        'username': getInfo('username'),
        'password': getInfo('password'),
    }, headers=headers)
    # print(resp.cookies)
    res = session.post(urlBaseNew + '/auth/adoptLegacyAuth', headers = {'x-uestc-bbs': '1'})
    # print(res.json()['data']['authorization'])
    setInfo('authorization', res.json()['data']['authorization'])
    session.headers['authorization'] = getInfo('authorization')

def getReplyListNew(tid: int, page: int = 1, pageSize: int = 10):
    res = session.get(urlBaseNew + f'/post/list?thread_id={tid}&page={page}&page_size={pageSize}thread_details=1&forum_details=0')
    if res.json()['code'] == 0:
        return res.json()['data']['rows']
    else:
        # print(res.request.headers)
        return []

def getHot10():
    paramsHot10 = {
        'r': 'portal/newslist',
        'moduleId': 2
    }
    res = requests.post(urlBase, params=paramsHot10, headers=headers)
    if res.json()['rs'] == 1:
        hot_list = res.json()['list']
        # pprint(hot_list)
        idx = 0
        for item in hot_list:
            user_id = item.get('user_id', 'N/A')
            user_nick_name = item.get('user_nick_name', 'N/A')
            title = item.get('title', 'N/A')
            sourceWebUrl = item.get('sourceWebUrl', 'N/A')
            print(f"{idx} user_id: {user_id} user_nick_name: {user_nick_name}, title: {title}, sourceWebUrl: {sourceWebUrl}")
            idx += 1
        return hot_list
    else:
        print(res.json()['errcode'])
        return []

def reply(tid, content):
    replycontent = [{'type': 0,'infor': content}]
    replyjson = {
        'body': {
            'json': {
                'tid': tid, 
                'content': json.dumps(replycontent),
            }
        }
    }

    paramsReply = {
        'r': 'forum/topicadmin',
        'act': 'reply',
        'apphash': getAppHashValue(),
        'accessToken': getInfo('token'),
        'accessSecret': getInfo('secret')
    }
    data1 = { 'act': 'reply', 'json': json.dumps(replyjson) }
    res = requests.post(urlBase, params=paramsReply, headers=headers, data=data1)
    try:
        if res.json()['rs'] == 1:
            pprint(strings[7])
        else:
            pprint(res.json())
    except:
        print(res.text)