#coding: utf-8

import time, datetime, hashlib
from math import radians, cos, sin, asin, sqrt

def utc2local(utc_dt):
    """UTC时间转本地时间"""
    now_stamp = time.time()
    local_time = datetime.datetime.fromtimestamp(now_stamp)
    utc_time = datetime.datetime.utcfromtimestamp(now_stamp)
    return utc_dt + (local_time - utc_time)

def local2utc(local_dt):
    """本地时间转UTC时间"""
    time_struct = time.mktime(local_dt.timetuple())
    utc_dt = datetime.datetime.utcfromtimestamp(time_struct)
    return utc_dt

def haversine(lon1, lat1, lon2, lat2):
    '''
        半正矢公式 计算两经纬度之间的距离
        
        lon1：经度1，
        lat1：纬度1，
        lon2：经度2，
        lat2：纬度2 （十进制度数）
    '''
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])  
    dlon = lon2 - lon1   
    dlat = lat2 - lat1
    
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2  
    c = 2 * asin(sqrt(a))   
    r = 6371
    return c * r * 1000  

def toString(obj):
    if(obj == None):
        return ""
    return str(obj)

def strToMD5(oriStr):
    m1 = hashlib.md5()   
    m1.update(oriStr.encode("utf8"))
    return m1.hexdigest()
    
