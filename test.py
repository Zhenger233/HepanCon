from fun import getAppHashValue, login, getInfo, setInfo, checkLogin, getHot10, reply
from strs import strings
from urllib.parse import quote

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
        sourceWebUrl = item.get('sourceWebUrl', 'N/A')
        hits = item.get('hits', '0')
        board = item.get('board_name', 'N/A')
        url_s += f'{sourceWebUrl}\n'
        res += f'[tr][td]{idx}[/td][td]{user_nick_name}[/td][td]{title}[/td][td]{summary}[/td][td]{replies}[/td][td]{hits}[/td][td]{board}[/td][/tr]\n'
        idx += 1
    res += '[/table]\n'
    res += url_s
    return res

def testHot10():
    l = getHot10()
    print(hot10list2str(l))

def testStrings():
    print(strings)

def testReply():
    l = getHot10()
    s = hot10list2str(l[0:1])
    reply(2224730, s)

if __name__ == '__main__':
    # testLogin()
    # testHot10()
    testReply()