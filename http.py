# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import logging
import json
import urllib
import random

url = 'http://dynamic.goubanjia.com/dynamic/get/d4a635a2fd4c265fff5fb2ab19f7fd06.html?random=yes'
data = urllib2.urlopen(url).read()
data = data.replace('\n','')
data = data.split(':',1)
res = urllib.urlopen(url).read().strip("\n");
ips = res.split("\n");
# 随机选择一个IP
proxyip = random.choice(ips)
print proxyip
targetUrl = 'http://weibo.cn/'
html = urllib.urlopen(targetUrl, proxies={'http':'http://' + proxyip})
print html.read()

