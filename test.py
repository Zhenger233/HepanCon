import os, sys
current_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_directory)
from fun import getAppHashValue, login, getInfo, setInfo, checkLogin, getHot10, reply, getReplyList, getNewAuth, session, getReplyListNew
from strs import strings
from urllib.parse import quote
import requests, json, re

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

def hot10list2str(hot10list: list) -> str:
    res = '[table][tr][td]Index[/td][td]User[/td][td]Title[/td][td]Summary[/td][td]Replies[/td][td]Hits[/td][td]Board[/td][/tr]\n'
    idx = 0
    url_s = ''
    for item in hot10list:
        user_id = item.get('user_id', '1')
        user_nick_name = item.get('user_nick_name', 'N/A')
        title = item.get('title', 'N/A')
        summary = item.get('summary', 'N/A')
        replies = item.get('replies', '0')
        sourceWebUrl = '/' + re.sub('.*/', '', item.get('sourceWebUrl', 'N/A'))
        hits = item.get('hits', '0')
        board = item.get('board_name', 'N/A')
        url_s += f'{sourceWebUrl}\n'
        res += f'[tr][td]{idx}[/td][td]{user_nick_name}[/td][td][url={sourceWebUrl}]{title}[/url][/td][td]{summary}[/td][td]{replies}[/td][td]{hits}[/td][td]{board}[/td][/tr]\n'
        idx += 1
    res += '[/table]\n'
    # res += url_s
    return res

def testHot10():
    l = getHot10()
    print(hot10list2str(l))

def testStrings():
    print(strings)

def testReplyHot10():
    login(myUsername, myPassword)
    l = getHot10()
    s = hot10list2str(l[:3])
    reply(2225218, s)

def testZhihu():
    res = requests.get('https://api.cenguigui.cn/api/juhe/hotlist.php?type=zhihu', timeout=5)
    data = res.json()['data']
    # print(data)
    s = '[table][tr][td]Index[/td][td]Title[/td][td]Hot[/td][td]qid[/td][/tr]\n'
    for item in data:
        idx = item['index']
        title = item['title']
        hot = item['hot']
        qid = re.sub(r'\D', '', item['url'])
        s += f'[tr][td]{idx}[/td][td]{title}[/td][td]{hot}[/td][td]{qid}[/td][/tr]\n'
    return s

def testGetReplyList():
    l = getReplyList(2225218, 1, 50)
    sys.stdout.reconfigure(encoding='utf-8')
    print(json.dumps(l, indent=4, ensure_ascii=False))
    # for r in l:
    #     if r['reply_id'] != 217527 or r['reply_content']

def testGetPeplyListNew():
    getNewAuth()
    l = getReplyListNew(2225218, 1)
    sys.stdout.reconfigure(encoding='utf-8')
    # print(json.dumps(l, indent=4, ensure_ascii=False))
    for r in l:
        if r['author_id'] == 217527 and 'viewthread' in r['message']:
            s = r['message']
            s1 = s[7:s.find('[/table]')]
            pattern = re.compile(r'\[tr\](.*?)\[/tr\]', re.DOTALL)
            rows = pattern.findall(s1)[1:]
            for row in rows:
                cells = re.findall(r'\[td\](.*?)\[/td\]', row, re.DOTALL)
                print(cells)

if __name__ == '__main__':
    # testLogin()
    # testHot10()
    # testReplyHot10()
    # testZhihu()
    # testGetReplyList()
    # checkLogin()
    testGetPeplyListNew()
    ...
