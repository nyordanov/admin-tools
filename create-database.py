#!/usr/bin/python3

import os
import getpass
import lib.vamtam as vamtam
import MySQLdb as MS
from colorama import Fore, Back, Style

print("Create database", "")

mysql_user = vamtam.option("Mysql user")
mysql_pass = getpass.getpass("%s password:" % mysql_user)
mysql_database = vamtam.option("Enter new database name")

if(vamtam.confirm('Creating database %s with user %s' % (mysql_database, mysql_user), True)):
	db1 = MS.connect(host="localhost",user=mysql_user,passwd=mysql_pass)
	cursor = db1.cursor()
	sql = 'CREATE DATABASE %s'
	cursor.execute(sql)

	if(vamtam.confirm('Create new database user?', True)):
		new_user = vamtam.option("Username", True, mysql_database)
		new_pass = vamtam.option("Password", True, vamtam.password_generator(25))

		sql = "grant all on %(db)s.* to %(user)s identified by %(pass)s"
		cursor.execute(sql, {
			'db': mysql_database,
			'user': new_user,
			'pass': new_pass
		});

		cursor.execute('flush privileges');

		print("")
		print('Created database '+Fore.RED+mysql_database++Style.RESET_ALL)
		print('Access with user '+Fore.RED+new_user+Style.RESET_ALL' and '+Fore.RED+new_pass+Style.RESET_ALL)
	else:
		print('Created database '+Fore.RED+mysql_database+Style.RESET_ALL)
		exit(0)
else:
	print("abort")
	exit(0)