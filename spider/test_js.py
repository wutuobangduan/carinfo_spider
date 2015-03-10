# coding:utf-8
import os
import tempfile
 
def call_js(js):
 
    f=tempfile.mktemp()
    f2=tempfile.mktemp()
 
    fp=open(f,'w')
    fp.write(js)
    fp.close()
 
    cmd="/usr/local/bin/js  %s > %s" % (f,f2)
 
    os.system(cmd)
    result=open(f2).read()
    print result
if __name__ == "__main__":
    code='''
    function dF(s,n){
        n=parseInt(n);
        var s1=unescape(s.substr(0,n)+s.substr(n+1,s.length-n-1));
        var t='';
        for(var i=0;i<n;i++)
            t+=String.fromCharCode(s1.charCodeAt(i)-s.substr(n,1));
        return(unescape(t));
    }
    print(dF('89gig37h5h68d%3C%3A8938i86%3C%3A%3Cf%3C63h87h',21));
    print(dF('%3Ahe56e36h6dd37e%3B98g%3Aec456ggd32e28',37))
    '''
    call_js(code);
