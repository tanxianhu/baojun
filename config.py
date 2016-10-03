#coding=utf-8

#dbs Config


mdbMCfg = {
	'pool_name': 'mdbMpool',
	'pool_size': 2,
	'host': '192.168.1.36',
	'port': 3306,
	'user': 'root',
	'password': 'sddkhhyy.0.',
	'database': 'BJST',
	'charset': 'utf8'
	}

rcNodes = [{"host": "192.168.10.4", "port": "6000"},
           {"host": "192.168.10.4", "port": "6001"},
           {"host": "192.168.10.4", "port": "6002"},
           {"host": "192.168.10.4", "port": "6003"},
           {"host": "192.168.10.4", "port": "6004"},
           {"host": "192.168.10.4", "port": "6005"}]

mgoMUrl = 'mongodb://baifz:baifz3.1415@127.0.0.1:27017/bfz'
mgoAUrl = 'mongodb://baifz:baifz3.1415@127.0.0.1:27017/antnest'
mgoSUrl = 'mongodb://127.0.0.1:27017/bfzdb'

mqttCfg={"ip":"10.163.112.27","port":11883,"user":"appserver","pwd":"123456abc"}
