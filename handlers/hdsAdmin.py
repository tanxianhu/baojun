#coding=utf-8

import os
import tornado.web

#import tor_access
from handlers import tor_access
from handlers.BHandlers import BaseHandler
from handlers.base import admin_config
from handlers.base import api_log
import json


@tor_access.needcheck(url=True, category='系统管理组')
class AclRolesListHandler(BaseHandler, admin_config.RolesHandler):
    """权限管理：
    自动采集完成，-1：旧的，可剔除；0：系统定义；1：新增，待上线；2：上线，授权使用。
    """
    @tornado.web.authenticated
    def get(self):
        self.render("admin/acl_roles.html")
        
    @tornado.web.authenticated
    def post(self):
        self.check_rules()
        mResult = self.getRolesList()
        self.write(mResult)
        self.finish()


@tor_access.needcheck(url=True, category='系统管理组')
class AclRolesOnOffHandler(BaseHandler, admin_config.RolesHandler):
    """权限管理：权限上-下线"""
    @tornado.web.authenticated
    def post(self):
        self.check_rules()
        mResult = self.modRolesStatus()
        self.write(mResult)
        self.finish()
        

@tor_access.needcheck(url=True, category='系统管理组')
class AclUsersListHandler(BaseHandler, admin_config.UsersRolesHandler):
    """权限管理：用户权限信息查看。"""
    @tornado.web.authenticated
    def get(self):
        self.render("admin/acl_users.html")
        
    @tornado.web.authenticated
    def post(self):
        self.check_rules()
        mResult = self.getUsersRolesList()
        self.write(mResult)
        self.finish()


@tor_access.needcheck(url=True, category='系统管理组')
class AclUsersGrantHandler(BaseHandler):
    """权限管理：授权管理。"""
    @tornado.web.authenticated
    def get(self):
        self.render("admin/acl_users_grant.html")

    @tornado.web.authenticated
    def post(self):
        self.check_rules()
        print(self.request.body)
        aclop = self.get_argument("aclop", 'show')
        
        mResult = {}
        if aclop == "grant":
            userId = self.get_argument("userId", '')
            opvalue = self.get_argument("opvalue", '')
            handler = self.get_argument("handler", None)
            mResult = self.aclGrant(userId, handler, opvalue)
        elif aclop == "revoke":
            userId = self.get_argument("userId", '')
            opvalue = self.get_argument("opvalue", '')
            handler = self.get_argument("handler", None)
            mResult = self.aclRevoke(userId, handler, opvalue)
        else:
            userId = self.get_argument("userId", '0')
            mUser = self.affirmUser(userId = userId)
            userId = mUser['userId']
            if userId in [None, '']:
                mResult['total'] = 0
                mResult['rows'] = []
                mResult['status'] = -1
                mResult['remark'] = "被授权ID为空。"
            else:
                mStatus = '2'
                whereStr = """ AND auh.user_id = '%s'
                              WHERE ar.`status` = '%s' """ % (str(userId), str(mStatus))
                mResult["total"] = self.getCount(whereStr)
                mResult['rows'] = self.getAclList(whereStr) if mResult["total"] > 0 else []
                mResult['user'] = mUser
        self.write(mResult)
        self.finish()

    def affirmUser(self, userId = None, accounts = None):
        """确认授权"""
        mResult = {'userId': '', 'realname': '', 'username': '', 'accounts': ''}
        sqlStr  = """SELECT u.`id`, u.realname, u.username, ua.accounts
                     FROM `bfzdb`.`user` AS u, `bfzdb`.`user_account` AS ua
                     WHERE u.id = ua.user_id """
        
        if userId not in [None, '']:
            sqlStr = sqlStr + " AND u.`id` = '%s'" % (str(userId))
        elif accounts not in [None, '']:
            sqlStr = sqlStr + " AND ua.accounts = '%s'" % (str(accounts))
        else:
            return mResult
        con = self.application.mdbMCli.get_connection()
        cur = con.cursor()
        cur.execute(sqlStr)
        row = cur.fetchone()
        cur.close()
        con.close()
        if row != None:
            mResult = {'userId': row[0], 'realname': row[1], 'username': row[2], 'accounts': row[3]}
        return mResult

    def aclGrant(self, userId, handler, opvalue):
        """授权"""
        mResult = {}
        userId = self.affirmUser(userId = userId)['userId']
        
        if userId in [None, '']:
            mResult['status'] = -1
            mResult['remark'] = "被授权ID为空。"
        elif handler in [None, '']:
            mResult['status'] = -1
            mResult['remark'] = "被授权,权限ID为空。"
        else:            
            sqlStr = """INSERT INTO `bfzdb`.acl_user_handler(`user_id`, `handler`, `opvalue`, `author`, `created`) 
                        VALUES ('%s', '%s', '%s', '%s', NOW())"""
            sqlStr = sqlStr %(str(userId), handler, opvalue ,self.current_user['userId'])
            con = self.application.mdbMCli.get_connection()
            cur = con.cursor()
            cur.execute(sqlStr)
            con.commit()
            cur.close()
            con.close()
            mResult['status'] = 0
            mResult['remark'] = "被授权,成功。"
            mResult['result'] = {'userId':userId,'handler':handler}
        return mResult
        

    def aclRevoke(self, userId, handler, opvalue):
        """撤销"""
        mResult = {}
        if userId in [None, '']:
            mResult['status'] = -1
            mResult['remark'] = "被撤销授权,用户ID为空。"
        elif handler in [None, '']:
            mResult['status'] = -1
            mResult['remark'] = "被销授授权,权限ID为空。"
        else:
            sqlStr = """DELETE FROM `bfzdb`.acl_user_handler WHERE user_id = '%s' AND `handler` = '%s'"""
            sqlStr = sqlStr % (str(userId), handler)
            con = self.application.mdbMCli.get_connection()
            cur = con.cursor()
            cur.execute(sqlStr)
            con.commit()
            cur.close()
            con.close()
            mResult['status'] = 0
            mResult['remark'] = "撤销授权,成功。"
            mResult['result'] = {'userId':userId,'handler':handler}
        return mResult
            

    def getCount(self, whereStr):
        """"""
        sqlStr  = """SELECT COUNT(ar.`handler`)
                     FROM `bfzdb`.acl_roles AS ar
                     LEFT JOIN `bfzdb`.acl_user_handler AS auh ON auh.`handler` = ar.`handler` """
        sqlStr += whereStr
        con = self.application.mdbMCli.get_connection()
        cur = con.cursor()
        cur.execute(sqlStr)
        mCount = cur.next()[0]
        cur.close()
        con.close()
        return mCount
        
    def getAclList(self, whereStr):
        """"""
        rows = int(self.get_argument("rows", '20'))
        page = int(self.get_argument("page", '1'))
        mLimit = rows if rows > 0 else 20
        mSkip = (page-1)*mLimit if page > 0 else 0
        
        mDataList = []
        sqlStr  = """SELECT
                       ar.`handler`, ar.category, ar.description,
                       IF(auh.`handler` = ar.`handler`, 'True', 'False') AS authorized
                     FROM `bfzdb`.acl_roles AS ar
                       LEFT JOIN `bfzdb`.acl_user_handler AS auh ON auh.`handler` = ar.`handler` """
        sqlStr += whereStr
        sqlStr += " ORDER BY ar.category, ar.`handler` LIMIT %s,%s " % (str(mSkip), str(mLimit))
        con = self.application.mdbMCli.get_connection()
        cur = con.cursor()
        cur.execute(sqlStr)
        for row in cur:
            acp = {}
            acp["handler"] = row[0]
            acp["category"] = row[1]
            acp["description"] = row[2]
            acp["authorized"] = row[3]            
            mDataList.append(acp)
        cur.close()
        con.close()
        return mDataList


@tor_access.needcheck(url=True, category='系统管理组')
class SysConfigListHandler(BaseHandler, admin_config.ConfigHandler):
    """系统配置：配置列表"""
    @tornado.web.authenticated
    def get(self):
        #self.check_rules()
        self.render("admin/sys_config_list.html")
        
    @tornado.web.authenticated
    def post(self):
        self.check_rules()
        mResult = self.getConfigList()
        self.write(mResult)
        self.finish()
        

@tor_access.needcheck(url=True, category='系统管理组')
class SysConfigAddHandler(BaseHandler, admin_config.ConfigHandler):
    """系统配置：增加"""
    
    @tornado.web.authenticated
    def post(self):
        self.check_rules()
        mResult = self.addConfig()
        self.write(mResult)
        self.finish()


@tor_access.needcheck(url=True, category='系统管理组')
class SysConfigModHandler(BaseHandler, admin_config.ConfigHandler):
    """系统配置：修改"""
    
    @tornado.web.authenticated
    def post(self):
        self.check_rules()
        mResult = self.modConfig()
        self.write(mResult)
        self.finish()


@tor_access.needcheck(url=True, category='系统管理组')
class SysConfigDelHandler(BaseHandler, admin_config.ConfigHandler):
    """系统配置：删除"""
    @tornado.web.authenticated
    def post(self):
        self.check_rules()
        mResult = self.delConfig()
        self.write(mResult)
        self.finish()
        
        
@tor_access.needcheck(url=True, category='系统管理组')
class ApiLogListHandler(BaseHandler, api_log.ApiLogHandler):
    """API日志管理：
    """
    @tornado.web.authenticated
    def get(self):
        self.render("admin/api_log_list.html")
        
    @tornado.web.authenticated
    def post(self):
        self.check_rules()
        mResult = self.getApiLogList()
        self.write(mResult)
        self.finish()


@tor_access.needcheck(url=True, category='系统管理组')
class SysConfigQueryHandler(BaseHandler, admin_config.ConfigHandler):
    """系统配置：删除"""
    @tornado.web.authenticated
    def post(self):
        self.check_rules()
        mResult = self.queryConfig()
        self.write(mResult)
        self.finish()
        
@tor_access.needcheck(url=True, category='系统管理组')
class BigCargoTypeHandler(BaseHandler, admin_config.CargoTypeHandler):
    """货物类型"""
    @tornado.web.authenticated
    def get(self):
        self.render("admin/big_cargo_type.html")
        
    @tornado.web.authenticated
    def post(self):
        self.check_rules()
        getAll = self.get_argument("getAll",None)
        if getAll in [None,""]:
            mResult = self.getCargoType()
        else:
            mResult = self.getAllCargoType()
            self.set_header("Content-Type","application/json")
            mResult = json.dumps(mResult)
           
        self.write(mResult)
        self.finish()
        
@tor_access.needcheck(url=True, category='系统管理组')
class BigCargoTypeAddHandler(BaseHandler, admin_config.CargoTypeHandler):
    """货物类型添加"""
        
    @tornado.web.authenticated
    def post(self):
        self.check_rules()
        mResult = self.addCargoType()
        self.write(mResult)
        self.finish()
        
@tor_access.needcheck(url=True, category='系统管理组')
class BigCargoTypeModHandler(BaseHandler, admin_config.CargoTypeHandler):
    """货物类型修改"""
        
    @tornado.web.authenticated
    def post(self):
        self.check_rules()
        mResult = self.modCargoType()
        self.write(mResult)
        self.finish()

@tor_access.needcheck(url=True, category='系统管理组')
class SmallCargoTypeHandler(BaseHandler, admin_config.SmallCargoTypeHandler):
    """货物小类类型"""
    @tornado.web.authenticated
    def get(self):
        self.render("admin/small_cargo_type.html")
        
    @tornado.web.authenticated
    def post(self):
        self.check_rules()
        mResult = self.getTypeList()
        self.write(mResult)
        self.finish()
        
@tor_access.needcheck(url=True, category='系统管理组')
class SmallCargoTypeAddHandler(BaseHandler, admin_config.SmallCargoTypeHandler):
    """货物小类类型添加"""
        
    @tornado.web.authenticated
    def post(self):
        self.check_rules()
        mResult = self.smallTypeInsert()
        self.write(mResult)
        self.finish()
        
@tor_access.needcheck(url=True, category='系统管理组')
class SmallCargoTypeModHandler(BaseHandler, admin_config.SmallCargoTypeHandler):
    """货物小类类型添加"""
        
    @tornado.web.authenticated
    def post(self):
        self.check_rules()
        mResult = self.smallTypeMod()
        self.write(mResult)
        self.finish()
        
@tor_access.needcheck(url=True, category='系统管理组')
class VehicleTypeHandler(BaseHandler, admin_config.VehicleTypeMainHandler):
    """车辆类型"""
    @tornado.web.authenticated
    def get(self):
        self.render("admin/vehicle_type_config.html")
        
        
    @tornado.web.authenticated
    def post(self):
        self.check_rules()
        mResult = self.getVehicleTypeList()
        self.write(mResult)
        self.finish()
@tor_access.needcheck(url=True, category='系统管理组')
class VehicleTypeModHandler(BaseHandler, admin_config.VehicleTypeMainHandler):
    """车辆类型修改"""
        
    @tornado.web.authenticated
    def post(self):
        self.check_rules()
        mResult = self.modVehicleType()
        self.write(mResult)
        self.finish()
@tor_access.needcheck(url=True, category='系统管理组')
class VehicleTypeAddHandler(BaseHandler, admin_config.VehicleTypeMainHandler):
    """车辆类型添加"""
        
    @tornado.web.authenticated
    def post(self):
        self.check_rules()
        mResult = self.addVehicleType()
        self.write(mResult)
        self.finish()


