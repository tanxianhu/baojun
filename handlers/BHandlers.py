#coding=utf-8

import datetime,json
import tornado.web

#import tor_access
from handlers import tor_access


class BaseHandler(tornado.web.RequestHandler):
    """
    """
    def get_current_user(self):
        curUser = self.get_secure_cookie("user")
        if curUser:
            curUser = eval(curUser.decode())
        else:
            mToken = self.get_argument("token", None)
            if mToken:
                db = self.application.mgoMCli['bfz']
                curUser = db.token_pool.find_one({"token":str(mToken)})
                if curUser:
                    curUser['userId'] = curUser['_id']
                    curUser.pop('_id')
        return curUser

    def check_rules(self):
        """获取用户所有权限,以及操作权"""
        userId = self.current_user['userId'] 
        conx = None
        #try:
        sqlFmt = """SELECT `handler` FROM `bfzdb`.`acl_user_handler` WHERE `user_id` = '%s';"""
        sqlStr = sqlFmt % (userId)
        curs = self.application.mysql.execQueryList(sqlStr)
            
            #conx = self.application.mdbMCli.get_connection()
            #curs = conx.cursor()
            #curs.execute(sqlStr)
            
        handlers = []
        for handler in curs:
            handlers.append(handler["handler"])
                
        opIdList = ['GET','POST','PUT','DELETE']
        self.request.method

        if "administrators" in handlers:
            # 超管角色；有所有的权限节点
            rn = tor_access.MasterRoleNeed()
        else:
            rn = tor_access.RoleNeed('abcrole',intro=u'普通角色',nodes=set(handlers), ctx_vals=set(opIdList))
                
        #except Exception as ex:
        #    print("check_rules:", ex)
        #finally:
        #    curs.close()
        #    conx.close()
        
        try:
            self.check_access(rn)
        except Exception as ex:
            raise tornado.web.HTTPError(403)


