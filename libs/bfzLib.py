#coding: utf-8

import time, datetime, re, urllib.request, json, ctypes, codecs
from random import Random


class bmResult:
    """通用返回对像"""
    def __init__(self):
        self.status = 0
        self.remark = None
        self.result = None
        
    def toJson(self):
        """method: toJson"""
        mJson = {"status" : self.status,
                 "remark" : self.remark,
                 "result" : self.result}
        return json.dumps(mJson)


class bmBilling:
    """Billing实体对像"""
    userId = 0
    account = ''
    validTime = ''
    orderStatus = 0
    orderBy = ''


class bmSales:
    """Sales实体对像"""
    qq = ''
    f_qq = ''
    payable = 0
    payment = 0
    depth = 0
    sales_status = 0
    created = ''


def bmPrint(msgStr, txtColor):
    """宝妹彩色Print(输出内容，前景颜色)"""
    h = ctypes.windll.Kernel32.GetStdHandle(ctypes.c_ulong(0xfffffff5))
    if txtColor == "W":#亮白
        ctypes.windll.Kernel32.SetConsoleTextAttribute(h, 15)
    elif txtColor == "Y":#黄色
        ctypes.windll.Kernel32.SetConsoleTextAttribute(h, 14)
    elif txtColor == "P":#紫色
        ctypes.windll.Kernel32.SetConsoleTextAttribute(h, 13)
    elif txtColor == "R":#红色
        ctypes.windll.Kernel32.SetConsoleTextAttribute(h, 12)
    elif txtColor == "G":#绿色
        ctypes.windll.Kernel32.SetConsoleTextAttribute(h, 10)
    elif txtColor == "B":#蓝色
        ctypes.windll.Kernel32.SetConsoleTextAttribute(h, 9)
    else:#乳白(默认)
        ctypes.windll.Kernel32.SetConsoleTextAttribute(h, 7)
    print (msgStr)
    ctypes.windll.Kernel32.SetConsoleTextAttribute(h, 7)#乳白(默认)


def utc2local(utc_st):
    """UTC时间转本地时间"""
    now_stamp = time.time()
    local_time = datetime.datetime.fromtimestamp(now_stamp)
    utc_time = datetime.datetime.utcfromtimestamp(now_stamp)
    return utc_st + (local_time - utc_time)

def local2utc(local_st):
    """本地时间转UTC时间"""
    time_struct = time.mktime(local_st.timetuple())
    utc_st = datetime.datetime.utcfromtimestamp(time_struct)
    return utc_st

def getTimestamp(strTime):
    return time.strptime(strTime,"%Y-%m-%d %H:%M:%S")


def getDatetime(dtString):
    return datetime.datetime.strptime(dtString,"%Y-%m-%d %H:%M:%S")


def getNowString():
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return dt


def getTimeDiff_t(tmp_dt):
    """获取时间差字符串(x分钟内、x小时内、x星期内、1星期以上)"""

    dt_diff = datetime.datetime.now() - tmp_dt
    #diff = dt_diff.total_seconds()
    diff = dt_diff.total_seconds() - 28800
    if diff < 60:
        return '1分钟内'
    elif diff < 3600:
        return str(int(diff/60) + 1) + '分钟内'
    elif diff < 86400:
        return str(int(diff/3600) + 1) + '小时内'
    elif diff < 604800:
        return str(int(diff/604800) + 1) + '星期内'
    elif diff > 604800:
        return '1星期以上'


def getTimeDiff(tmp_dt):
    """获取时间差字符串(x分钟内、x小时内、x星期内、1星期以上)"""
    dt_diff = datetime.datetime.now() - tmp_dt
    diff = dt_diff.total_seconds() - 28800
    #print(tmp_dt,'\n',dt_diff,'\n',diff)
    if diff < 60:
        return '1分钟内'
    elif diff < 3600:
        return str(int(diff/60) + 1) + '分钟内'
    elif diff < 86400:
        return str(int(diff/3600) + 1) + '小时内'
    elif diff < 604800:
        return '昨天 %d:%d' %(tmp_dt.hour,tmp_dt.minute)
    elif diff < 172800:
        return '前天 %d:%d' %(tmp_dt.hour,tmp_dt.minute)
    elif diff < 259200:
        return str(int(diff/604800) + 1) + '星期内'
    elif diff > 604800:
        return '1星期前'


def getValidDate(validTime = None, addays = 0):
    curTime = datetime.datetime.now()
    if validTime == None:
        validTime = curTime
    if curTime >= validTime:
        validTime = curTime
    validTime = validTime + datetime.timedelta(days=addays)
    validTime = validTime.strftime("%Y-%m-%d %H:%M:%S")
    return validTime
    
def phone_recognition(msgStr):
    re.findall(r"(\d{3,4}((\-|\s{1,2}|－|——)?\d{3,4}){2})", msgStr)

def is_moblie(mStr):
    """将要作废"""
    pMobl = re.compile('^1[345678]\d{9}$')
    pMatch = pMobl.match(mStr)
    if pMatch:
        return True
    else:
        return False

def isMail(mStr):
    """Email地址"""
    pMail = re.compile('[^\._-][\w\.-]+@(?:[A-Za-z0-9]+\.)+[A-Za-z]+$')
    pMatch = pMail.match(mStr)
    if pMatch:
        return (True, pMatch.group())
    else:
        return (False, '')

def isMoblie(mStr):
    """国内手机"""
    pHone = re.compile('^1[345678]\d{9}$')
    pMatch = pHone.match(mStr)

    if pMatch:
        return (True, pMatch.group())
    else:
        return (False, '')


def isPhone(mStr):
    """国内电话"""
    pHone = re.compile('^0\d{2,3}-?\d{7,8}$|^1[345678]\d{9}$')
    pMatch = pHone.match(str(mStr))

    if pMatch:
        return (True, pMatch.group())
    else:
        return (False, '')


def bmRequest(mUrl, mData = None):
    """http交互(get/post)str,str,ret(str)"""
    ret = ""
    try:
        mBodys = None
        if mData != None:
            mBodys = codecs.encode(mData,'utf-8')
        request = urllib.request.Request(mUrl, mBodys)
        request.add_header('Content-Type','application/json')
        response = urllib.request.urlopen(request)
        ret = response.read()
    except Exception as ex:
        print("Err: bmRequest Error!")
        ret = None
    return ret


def random_str(randomlength):
    """随机验证码字符"""
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str
