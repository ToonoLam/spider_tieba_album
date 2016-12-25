# -*- coding: utf-8 -*- 
'''
Created on 2016年8月10日

@author: toono
'''
# 引入模块
import os
import re
import socket
import sys
from tkFileDialog import askdirectory
import urllib
import urllib2

from bs4 import BeautifulSoup
import requests  
from itertools import count


try:
  import xml.etree.cElementTree as ET
except ImportError:
  import xml.etree.ElementTree as ET

def mkdir(path):
 
#    # 去除首位空格
#    path=path.strip()
#    # 去除尾部 \ 符号
#    path=path.rstrip("\\")
 
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)
 
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        print path + u' 创建成功'
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print path + u' 目录已存在'
        return False
 
def browser_gethtml(url):
    req_header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'}
    try:
#        gethtml = requests.get(url, req_header).text
        req = urllib2.Request(url,None,req_header)
        html_text = urllib2.urlopen(req,None,20).read()
        return html_text
    except urllib2.URLError as e:
        print e.message
    except socket.timeout as e:
        browser_gethtml(url)

def callbackfunc(blocknum, blocksize, totalsize):
    '''回调函数
    @blocknum: 已经下载的数据块
    @blocksize: 数据块的大小
    @totalsize: 远程文件的大小
    '''
    percent = 100.0 * blocknum * blocksize / totalsize
    if percent > 100:
        percent = 100
    print "下载中……"
    download_perc =  "%.2f%%"% percent
    print download_perc
    
'''获取用户输入的贴吧名'''
try:
#    tieba_kw = raw_input("请输入贴吧名: ")
    tieba_kw = '宇多田光'
    album_url = 'http://tieba.baidu.com/f?kw=%s&ie=utf-8&tab=album' % tieba_kw
    print "下载进度:"
    html_albums = requests.get(album_url)  
    
except: 
    print '\nthere are some errors'  
#获取所有相册名并于提供一个对话框选择保存路径,并在该路径下以各相册名建立文件夹
#mkpath_base = askdirectory(initialdir = u'F:\\\\宇多田光') + u'\\' + tieba_kw.decode("utf-8") + u"吧相册\\"

re_albumname_urltid = r'<a hidefocus="true" target="_blank" href="(.+?)" title="(.+?)">'
get_name = re.findall(re_albumname_urltid, html_albums.text)
for i in range(len(get_name)):
    mkpath_last = u'F:\\\\宇多田光' + u'\\' + tieba_kw.decode("utf-8") + u"吧相册\\" + get_name[i][1] + u"\\"# 定义要创建的目录
    mkdir(mkpath_last)# 调用函数
    #根据获得的相册url获取对应相册的html文档,解析出各个图片对应的html,并从对应html解析出图片源url
    photo_url = (u'http://tieba.baidu.com'+get_name[i][0]+u'#!/l/p1').encode("utf-8")
    re_tid = r'http://tieba.baidu.com/p/(.+?)#!/l/p1'
    tid = re.findall(re_tid, photo_url)[0]
    try:
        html_one_album = browser_gethtml(photo_url)
    except:
        print "socket timeout"
        html_one_album = ""
    re_pic_id = r'data-field="{pic_id:\'(.+?)\'}">'
    pic_ids = re.findall(re_pic_id, html_one_album)
    for pic_id in range(len(pic_ids)):
        url_pic = "http://tieba.baidu.com/photo/p?kw=%s&tid=%s&pic_id=%s" %(tieba_kw, tid, pic_ids[pic_id].encode('utf-8'))
        try:
            response_html = requests.get(url_pic).text
            
        except:
            print "读取下载页页面html数据时失败"
        re_pic = r'url":"(http://imgsrc.baidu.com/forum/.+?.jpg)'
        url = re.findall(re_pic, response_html)[0]
        local = mkpath_last + pic_ids[pic_id].decode('utf-8') + u'.jpg'
        if not os.path.exists(local):
            try:
                output = open(local,'wb+')
            except:
                print "图片加载失败"
            finally:
                output.close()
                
            try:
                urllib.urlretrieve(url, local, callbackfunc)
                
                print local + '……下载成功'
            except:
                print "无法下载图片: " + pic_ids[pic_id] + '.jpg'
            
print "\n该程序结束"