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

def get_kw():
    '''获取用户输入的贴吧名'''
    try:
        TIEBA_KW = raw_input("请输入贴吧名: ")
        is_true_url = 'http://tieba.baidu.com/f/search/fm?ie=UTF-8&qw=%s' % TIEBA_KW
        html_is_true = requests.get(is_true_url)
        re_true = u'href=\"\/f\?kw=%s\"' % TIEBA_KW.decode('utf-8')
        if len(re.findall(re_true, html_is_true.text)):
            return TIEBA_KW
        else:
            print "该贴吧不存在请重新输入"
            get_kw()
    except: 
        print '\n获取用户输入的贴吧名时发生未知错误'  
        os._exit(0)
        
def browser_gethtmltxt(url, cnt_most):
    #url = 需解析的网页地址(str), cnt_timeout = socket超时重连尝试最大次数(int)
    cnt_timeout = cnt_most
    cnt_connect = cnt_most
    req_header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'}
    try:
        html_text = requests.get(url, req_header).text
        return html_text
#    except urllib2.URLError as e:
#        print e.message
        os._exit(0)
    except socket.timeout as e:
        cnt_timeout -= 1
        if cnt_timeout == 0 :
            print '该地址尝试了%s次仍无法解析: \n' % cnt_most + url
            cnt_timeout = 0
            print e.message
            os._exit(0)
        else:
            browser_gethtmltxt(url, cnt_timeout)
    except requests.exceptions.Timeout as e:
        print e.message
        os._exit(0)
    except requests.exceptions.ConnectionError as e:
        
        cnt_connect -= 1
        if cnt_connect == 0 :
            print '该地址尝试了%s次仍无法连接: \n' % cnt_most + url
            cnt_connect = 0
            print e.message
            os._exit(0)
        else:
            browser_gethtmltxt(url, cnt_connect)
        
def mkdir(path):
    if not os.path.exists(path):
        # 如果不存在则创建目录
        print path + u' 创建成功'
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print path + u' 目录已存在'
        return False 
    
class DownloadFromHtml:
    DL_url = ''
    localurl = u''
    def __init__(self, DL_url, localurl):
        self.DL_url = DL_url
        self.localurl = localurl
        
    def __callbackfunc(self, blocknum, blocksize, totalsize):
        '''回调函数
        @blocknum: 已经下载的数据块
        @blocksize: 数据块的大小
        @totalsize: 远程文件的大小
        '''
        percent = 100.0 * blocknum * blocksize / totalsize
        if percent > 100:
            percent = 100
        download_perc =  "%.2f%%"% percent
        self.download_perc = download_perc

    def __create_picfile(self, localurl):
        try:
            output = open(localurl,'wb+')
        except:
            print "图片加载失败"
        finally:
            output.close()
        
    def DL_pic(self, pic_id):
        if not os.path.exists(self.localurl):
            self.__create_picfile(self.localurl)
            try:
                urllib.urlretrieve(self.DL_url, self.localurl, self.__callbackfunc())
                if self.download_perc == '100.00%':
                    print self.localurl + "……下载完成"
            except:
                print "无法下载图片: " + pic_id + '.jpg'


def main():
    TIEBA_KW = get_kw()#获取用户输入的贴吧名
    BASE_PATH = askdirectory(initialdir = u'F:\\\\宇多田光')#提供对话框选择保存路径
    
    albums_url = 'http://tieba.baidu.com/f?kw=%s&ie=utf-8&tab=album' % TIEBA_KW
    html_albums = browser_gethtmltxt(albums_url, 5)  
    re_albumname_urltid = r'<a hidefocus="true" target="_blank" href="(.+?)" title="(.+?)">'
    tid_and_name = re.findall(re_albumname_urltid, html_albums)
    print "下载详情:"
    for (p_tid, album_name) in tid_and_name:
        album_url = 'http://tieba.baidu.com%s#!/l/p1' % p_tid.encode("utf-8")
        html_one_album = browser_gethtmltxt(album_url, 5)
        re_pic_id = r'data-field="{pic_id:\'(.+?)\'}">'
        pic_ids = re.findall(re_pic_id, html_one_album)
        tid = p_tid.encode("utf-8")[3:]
        mkpath = u'%s\\%s吧相册\\%s\\' % (BASE_PATH, TIEBA_KW.decode("utf-8"), album_name)
        mkdir(mkpath)
        for pic_id in pic_ids:
            pic_url = "http://tieba.baidu.com/photo/p?kw=%s&tid=%s&pic_id=%s" %(TIEBA_KW, tid, pic_id.encode('utf-8'))
            html_pic = browser_gethtmltxt(pic_url, 5)
            re_pic = r'url":"(http://imgsrc.baidu.com/forum/.+?.jpg)'
            DL_url = re.findall(re_pic, html_pic)[0]
            pic_localurl = mkpath + pic_id.decode('utf-8') + u'.jpg'
            dl_pic = DownloadFromHtml(DL_url, pic_localurl)
            dl_pic.DL_pic(pic_id)
            
if __name__ == '__main__':
    main()
    print "\n该程序结束"


