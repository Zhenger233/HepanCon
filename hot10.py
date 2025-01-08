#!/usr/bin/env python3
from fun import login, getInfo, getHot10, reply
import requests, re
myUsername = getInfo('username')
myPassword = getInfo('password')

def getZhihu():
    res = requests.get('https://api.cenguigui.cn/api/juhe/hotlist.php?type=zhihu', timeout=5)
    data = res.json()['data']
    # print(data)
    s = '[table][tr][td]Index[/td][td]Title[/td][td]Hot[/td][td]qid[/td][/tr]\n'
    for item in data:
        idx = item['index']
        title = item['title']
        hot = item['hot']
        qid = re.sub('\D', '', item['url'])
        s += f'[tr][td]{idx}[/td][td]{title}[/td][td]{hot}[/td][td]{qid}[/td][/tr]\n'
    return s+'[/table]\n'

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
        url_s += f'{sourceWebUrl}&idx={idx}\n'
        res += f'[tr][td]{idx}[/td][td]{user_nick_name}[/td][td][url={sourceWebUrl}]{title}[/url][/td][td]{summary}[/td][td]{replies}[/td][td]{hits}[/td][td]{board}[/td][/tr]\n'
        idx += 1
    res += '[/table]\n'
    res += getZhihu()
    # res += url_s
    return res

def testReplyHot10():
    login(myUsername, myPassword)
    l = getHot10()
    s = hot10list2str(l)
    reply(2225218, s)

if __name__ == '__main__':
    # testLogin()
    # testHot10()
    testReplyHot10()
    ...
    
# 30 21 * * * cd /home/zz/gits/HepanCon;/home/zz/gits/HepanCon/hot10.py
