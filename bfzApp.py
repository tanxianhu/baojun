#coding=utf-8

import os,sys
import tornado.ioloop, tornado.web
import mysql.connector.pooling,pymongo,config

from handlers import tor_access
from handlers import BHandlers
from libs.MySqlUtils import MySqlUtils
from tornado.options import define,options,parse_command_line
from handlers import hdsServices

define("port", default=80, help="run on the given port", type=int)

settings = {
    "static_path" : os.path.join(os.path.dirname(__file__), "static"),
    "template_path" : os.path.join(os.path.dirname(__file__), "templates"),
    "cookie_secret" : "bfzKeyLdTP1XVJFuX7oEEhouKXQTmGJzGY6o5gAeE1nQp2aYd",
    "login_url": "/signin",
    'xsrf_cookies': False,
    "gzip" : True,
    }

apps = tornado.web.Application([
    (r"/(favicon\.ico)", tornado.web.StaticFileHandler, dict(path=settings['static_path'])),
    (r"/", hdsServices.IndexHandler),
    (r"/user/login", hdsServices.LoginHandler),
    (r"/msg/detail", hdsServices.MsgDetailHandler),
    (r"/user/phone/auth", hdsServices.PhoneAuthHandler),

    (r"/user/register/choseaddress", hdsServices.RegistarChoseAddrHandler),
    (r"/user/register/setpwd", hdsServices.RegisterSetPwdHandler),
    (r"/user/reset/pwd", hdsServices.ResetPwdHandler),
    (r"/user/info", hdsServices.UserInfoHandler),
    
    (r"/msg/my/scheme", hdsServices.MySehemeHandler),
    (r"/msg/publish", hdsServices.MsgPublishHandler),
    (r"/user/reset/pwd/phone/auth", hdsServices.ResetPwdPhoneAuthHandler),
    (r"/user/reset/pwd/suf", hdsServices.ResetPwdSufHandler)

    ],**settings)

apps.mysql = MySqlUtils()
apps.uploadPath=os.path.dirname(__file__)
apps.mgoMCli = pymongo.MongoClient(config.mgoMUrl)
apps.uploadPath=os.path.join(apps.uploadPath,'static')

if __name__ == "__main__":
    parse_command_line()
    print('Baifz Management System.')
    apps.listen(options.port)
    print('Management System Started. Listen Port: %s ' % (str(options.port)))
    print('---------------- -------------- ---------------- --------------')
    tornado.ioloop.IOLoop.instance().start()
	



