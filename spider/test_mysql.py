#!/usr/bin/env python
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='dp')
curs = conn.cursor()
conn.select_db('spider')
curs.execute("select id from yiche_qiugou_info where url='http://www.taoche.com/qiugou/650622.html'")
getrows=curs.fetchall()
if not getrows:
    print 'There is no data...'

for id in getrows:
    print '%s' % id

conn.commit()
curs.close()
conn.close()
