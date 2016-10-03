#coding=utf-8

import os
import tornado.web

from handlers import tor_access
from handlers.BHandlers import BaseHandler
import json

class IndexHandler(BaseHandler):
    #@tornado.web.authenticated
    def get(self):
        self.render("index.html")

    #@tornado.web.authenticated
    def post(self):
        self.check_rules()
        mResult = self.getVehicleTypeList()
        self.write(mResult)
        self.finish()

class LoginHandler(BaseHandler):
    #@tornado.web.authenticated
    def get(self):
        self.render("login.html")

class MsgDetailHandler(BaseHandler):
    #@tornado.web.authenticated
    def get(self):
        self.render("msgdetail.html")

class PhoneAuthHandler(BaseHandler):
    #@tornado.web.authenticated
    def get(self):
        self.render("phoneauth.html")

class RegistarChoseAddrHandler(BaseHandler):
    #@tornado.web.authenticated
    def get(self):
        self.render("registerchoseaddress.html")

class RegisterSetPwdHandler(BaseHandler):
    #@tornado.web.authenticated
    def get(self):
        self.render("registersetpwd.html")

class ResetPwdHandler(BaseHandler):
    #@tornado.web.authenticated
    def get(self):
        self.render("changepwd.html")

class UserInfoHandler(BaseHandler):
    #@tornado.web.authenticated
    def get(self):
        self.render("userInfo.html")
        
class MySehemeHandler(BaseHandler):
    #@tornado.web.authenticated
    def get(self):
        self.render("myScheme.html")

class MsgPublishHandler(BaseHandler):
    #@tornado.web.authenticated
    def get(self):
        self.render("publish.html")

class ResetPwdPhoneAuthHandler(BaseHandler):
    """车辆类型"""
    #@tornado.web.authenticated
    def get(self):
        self.render("resetpwdphoneauth.html")

class ResetPwdSufHandler(BaseHandler):
    """车辆类型"""
    #@tornado.web.authenticated
    def get(self):
        self.render("changepwdsuf.html") 
