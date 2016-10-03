#coding=utf-8

import os, datetime
import mysql.connector.pooling
import config

mysqlConnPool = mysql.connector.pooling.MySQLConnectionPool(**config.mdbMCfg)

class MySqlUtils:
    """mysql管理类"""
    
    def execQueryList(self,sqlStr,headerList = None):
        conn = mysqlConnPool.get_connection()
        cur = conn.cursor()
        
        ResultList = []
        item = {}
        headers = []
        try:
            cur.execute(sqlStr)
            if headerList != None and len(headerList)>0:
                headers = headerList
            else:
                headers = cur.description
                headers = [r[0] for r in headers ]
            for row in cur:
                item = {}
                for i in range(len(headers)):
                    item[headers[i]] = row[i]
                ResultList.append(item)
        except Exception as ex:
            print(ex,sqlStr)
        finally:
            self.mysqlClose(cur)
            self.mysqlClose(conn)
        return ResultList
            
    def execQueryOne(self,sqlStr,headerList=None):
        conn = mysqlConnPool.get_connection()
        cur = conn.cursor()

        if sqlStr != None and "limit" not in sqlStr.lower():
            sqlStr = sqlStr.replace(";","") + " limit 0,1 "
        item = {}
        headers = []
        try:
            cur.execute(sqlStr)
            row = cur.fetchone()
            if headerList != None and len(headerList)>0:
                headers = headerList
            else:
                headers = cur.description
                headers = [r[0] for r in headers ]
                
            for i in range(len(headers)):
                item[headers[i]] = row[i] if row != None else None
        except Exception as ex:
            print(ex,sqlStr)
        finally:
            self.mysqlClose(cur)
            self.mysqlClose(conn)
        return item
    
    def execUpdate(self,sqlStr):
        conn = mysqlConnPool.get_connection()
        cur = conn.cursor()
        item = {"effect":0,"lastrowid":""}
        try:
            cur.execute(sqlStr)
            item["lastrowid"]= int(cur.lastrowid)
            item["effect"]= cur.rowcount
            conn.commit()
        except Exception as ex:
            print(ex,sqlStr)
        finally:
            self.mysqlClose(cur)
            self.mysqlClose(conn)
        return item
    
    def mysqlClose(self,cur):
        try:
            b = cur.close() if cur != None else ""
        except Exception as ex:
            print(ex)
        finally:
            pass
        return True;
    
