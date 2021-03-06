import MySQLdb as db
import cgi
import os
import sys
import shutil
import datetime
import time
import hashlib
from random import randrange

print "Content-Type: text/plain\n"

try:
	con=db.connect('localhost','johnsondy','password','johnsondy')
	cur=con.cursor()
except db.Error, e:
	print e 
	sys.exit(1)

form=cgi.FieldStorage()

def GenFileName():
	ti=time.time()
	ts=datetime.datetime.fromtimestamp(ti).strftime('%Y-%m-%d %H:%M:%S')
	tsString=str(ts)
	tsHash=hashlib.sha224(tsString).hexdigest()
	tsHash=str(tsHash)
	fiName=""
	while (True):
		fiName=""
		for x in range(0,10,1):
			hashDig=randrange(0,len(tsHash)-1)
			fiName+=tsHash[hashDig]
		cur.execute("SELECT COUNT(filename) FROM filetable WHERE filename=%s",fiName)
		count=con.commit()
		if (count==None):
			cur.execute("INSERT INTO filetable (source,filename,filehash,lastaccess) VALUES (%s,%s,%s,%s)",(str(form['code'].value),fiName,tsHash,ts))
			con.commit()
			break
	return fiName

#Use this method if we need to delete projects that are older than a certain date.
def RemoveDeadProjects():
	ti=time.time()
	ts=datetime.datetime.fromtimestamp(ti)
	cur.execute("SELECT lastaccess FROM filetable")
	con.commit()
	loggedTime=cur.fetchall()
	for timestamp in loggedTime:
		diff=ts-timestamp[0]
		if (diff.days>31):#How old the projects are before they are deleted.
			cur.execute("DELETE FROM filetable WHERE lastaccess=%s LIMIT 1",(timestamp[0].strftime('%Y-%m-%d %H:%M:%S')))
			con.commit()

def UpdateLastAccess():
	ti=time.time()
	ts=datetime.datetime.fromtimestamp(ti).strftime('%Y-%m-%d %H:%M:%S')
	cur.execute("UPDATE filetable SET lastaccess=%s WHERE filename=%s",(str(ts),str(form['hash'].value)))
	con.commit()

if (int(form['pick'].value)==1):
	cur.execute("SELECT source FROM filetable WHERE filename=%s",(str(form['hash'].value)))
	con.commit()
	code=str(cur.fetchall())[3:-5]
	codeArray=code.split("\\n")
	for string in codeArray:
		print string
	UpdateLastAccess()

elif (int(form['pick'].value)==2):
	cur.execute("UPDATE filetable SET source=%s WHERE filename=%s",(str(form['code'].value),str(form['hash'].value)))
	con.commit()
	UpdateLastAccess()

elif (int(form['pick'].value)==3):
	fiName=GenFileName()
	print fiName
	
