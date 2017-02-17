import urllib2
import time

def check(proxy):
    import urllib2
    url = "http://www.baidu.com/js/bdsug.js?v=1.0.3.0"
    proxy_handler = urllib2.ProxyHandler({'http': "http://" + proxy})
    opener = urllib2.build_opener(proxy_handler,urllib2.HTTPHandler)
    try:
        response = opener.open(url,timeout=3)
        return response.code == 200
    except Exception:
        return False

def fetch_all(endpage=2):
    proxyes = []
    try:
        for i in range(5):
            url = 'http://dynamic.goubanjia.com/dynamic/get/d4a635a2fd4c265fff5fb2ab19f7fd06.html?random=yes'
            data = urllib2.urlopen(url).read()
            data = data.replace('\n','')
            data = data.split(':',1)
            ip = data[0]
            port = data[1]
            proxyes.append("%s:%s" % (ip, port))
            time.sleep(0.2)
    except Exception:
        pass
    return proxyes