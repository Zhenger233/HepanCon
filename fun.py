import hashlib
import time

def getMD5(s):
    return hashlib.md5(s.encode('utf-8')).hexdigest()

def getAppHashValue():
    s = f'{time.time()}'[:5] + 'appbyme_key'
    apphash = getMD5(s)
    ans = apphash[8:16]
    return ans
