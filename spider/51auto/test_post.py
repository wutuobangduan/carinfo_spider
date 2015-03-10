import urllib
import urllib2

test_data = {'callCount':1,'c0-scriptName':'CarViewAJAX','c0-methodName':'getCarInfoNew','c0-id':'3971_1421828644251','c0-param0':'number:2479037','xml':'true'}
test_data_urlencode = urllib.urlencode(test_data)

requrl = "http://www.51auto.com/dwr/exec/CarViewAJAX.getCarInfoNew"

req = urllib2.Request(url = requrl,data =test_data_urlencode)
print req

res_data = urllib2.urlopen(req)
res = res_data.read()
print res
