#!/usr/bin/python

import os
import getpass
import lib.vamtam as vamtam
import MySQLdb as MS
from lib.terminal import render

print "Create database", ""

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

		print ""
		print render('Created database %(RED)s%(BOLD)s'+mysql_database+'%(NORMAL)s')
		print render('Access with user %(RED)s%(BOLD)s'+new_user+'%(NORMAL)s and %(RED)s%(BOLD)s'+new_pass+'%(NORMAL)s')
	else:
		print render('Created database %(RED)s%(BOLD)s%(dbname)s%(NORMAL)s')
		exit(0)
else:
	print "abort"
	exit(0)