# -*- coding: utf-8 -*- 
#import requests
#
##获取图片下载网页源代码
#KW = '%E5%AE%87%E5%A4%9A%E7%94%B0%E5%85%89'
#tid = '1999653948'
#total_num = '153'
#url = 'http://tieba.baidu.com/photo/g/bw/picture/list?kw=%s&tid=%s&ps=1&pe=%s' % (KW, tid, total_num)
#
#html = requests.get(url).text
#with open('name.txt', 'wb') as f:
#    f.write(html.encode('utf-8'))
#    print "OK"
#    
#&alt=jview&rn=200
#import os
import re
from tkFileDialog import askdirectory

import requests


#import urllib2
#import json
# 
#html = urllib2.urlopen(r'http://api.douban.com/v2/book/isbn/9787218087351')
# 
#hjson = json.loads(html.read())
# 
#print (hjson['tags'][0]['name'], hjson['tags'][0]['count'])
#s = requests.session()
#url = 'http://imgsrc.baidu.com/forum/pic/item/dacc277f9e2f0708a22832daec24b899a801f2d1.jpg'
#src = s.get(url).content
#local_name = u'F:/\u5b87\u591a\u7530\u5149/\u5b87\u591a\u7530\u5149\u5427\u76f8\u518c/ Natural Breeze \u30c1\u30b1\u30c3\u30c8.jpg'
#
#def get_kw():
#    '''获取用户输入的贴吧名'''
#    try:
#        TIEBA_KW = raw_input("请输入贴吧名: ")
#        is_true_url = 'http://tieba.baidu.com/f/search/fm?ie=UTF-8&qw=%s' % TIEBA_KW
#        html_is_true = requests.get(is_true_url)
#        re_true = u'href=\"\/f\?kw=%s\"' % TIEBA_KW.decode('utf-8')
#        if len(re.findall(re_true, html_is_true.text)):
#            return TIEBA_KW
#        else:
#            print "该贴吧不存在请重新输入"
#            get_kw()
#    except: 
#        print '\n获取用户输入的贴吧名时发生未知错误'  
#        os._exit(0)
#
#KW = get_kw()
#BASE_PATH = askdirectory(initialdir = 'F:\\\\宇多田光').encode('utf-8')
#base_name = '尝试'
#album_path = '%s/%s吧相册/%s/' % (BASE_PATH, KW, base_name)
#
#descr = u'test'
#local = u'%s%s.jpg' % (album_path.decode('utf-8'), descr)
#with open(local, 'wb+') as f:
#    f.write(s.get(url).content)
    
import os

path = u'F:\宇多田光\宇多田光吧相册'    #获取当前路径
print sum([len(x) for _, _, x in os.walk(os.path.dirname(path))])