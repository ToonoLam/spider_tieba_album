#!/usr/bin/python2
# -*- coding: utf-8 -*-
import Tkinter
import os
import re
from tkFileDialog import askdirectory

from lxml import html
import requests

''''''

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

def mkdir(path):
    if not os.path.exists(path):
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
#        print path + u' 目录已存在'
        return False 

def etree_to_string(etree_name):
    etree_string = []
    for name in etree_name:
        if name.encode('utf-8').strip() != '':
            etree_string.append(name.encode('utf-8').strip())
    return etree_string

def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/\:*?"<>|'
    new_title = re.sub(rstr, "", title)
    return new_title
        
#def openurl(url): 
#    try:
#        req_header = {'Connection' : 'keep-alive'}
#        s = requests.session()
#        html = s.get(url, headers = req_header)
#        return html
#    except requests.exceptions.ConnectionError as e:
#        print "has connectionerror and return"
#        os._exit(0)

headers = {'Connection' : 'keep-alive'}
s = requests.session()

TIEBA_KW = get_kw()#获取用户输入的贴吧名
root = Tkinter.Tk()
BASE_PATH = askdirectory(initialdir = 'F:\\\\宇多田光').encode('utf-8')#提供对话框选择保存路径
root.withdraw()

'''第一个页面'''
#KW = '%E5%AE%87%E5%A4%9A%E7%94%B0%E5%85%89'
url_base_album = 'http://tieba.baidu.com/f?kw=%s&tab=album' % TIEBA_KW
page_base_album = s.get(url_base_album, headers = headers)
tree_base_album = html.fromstring(page_base_album.text)

#获取贴吧图册名
xpath_base_name = '//*[@class="catalog_a_inner"]/text()'
base_name = etree_to_string(tree_base_album.xpath(xpath_base_name))[1:]
#获取各图册的cat_id
xpath_base_cat_id = '//*[@class="j-catlog-item "]/@href'
base_cat_id = etree_to_string(tree_base_album.xpath(xpath_base_cat_id))
list_base_album = []
for i in xrange(len(base_name)):
    list_base_album.append((base_name[i],base_cat_id[i]))

'''从这可以建立根目录'''


for base_name, cat_id in list_base_album:
    '''第二个页面'''
    url_sub_album = 'http://tieba.baidu.com' + cat_id
    page_sub_album = s.get(url_sub_album, headers = headers)
    tree_sub_album = html.fromstring(page_sub_album.text)
    
    #获取各图册的相册名
    xpath_albums_name = '//*[@class="grbm_ele_title"]/a/@title'
    album_name = etree_to_string(tree_sub_album.xpath(xpath_albums_name))
    #获取各相册的tid
    xpath_albums_tid = '//*[@class="grbm_ele_title"]/a/@href'
    album_tid = etree_to_string(tree_sub_album.xpath(xpath_albums_tid))
    #获取各相册的total_num
    xpath_albums_total_num = '//*[@class="grbm_ele_a grbm_ele_big"]/span/text()'
    album_total_num = etree_to_string(tree_sub_album.xpath(xpath_albums_total_num))
    
    #判断是否有多的页数
    xpath_frs_list_pager = '//*[@class=" pagination-item "]/text()'
    base_frs_list_pager = etree_to_string(tree_sub_album.xpath(xpath_frs_list_pager))
    if len(base_frs_list_pager):
        for page in base_frs_list_pager:
            url = url_sub_album + '&pn=%s' % page
            urlhtml = s.get(url, headers = headers)
            tree_html = html.fromstring(urlhtml.text)
            #获取各图册的相册名
            xpath_name = '//*[@class="grbm_ele_title"]/a/text()'
            others_name = etree_to_string(tree_html.xpath(xpath_name))
            #获取各相册的tid
            xpath_tid = '//*[@class="grbm_ele_title"]/a/@href'
            others_tid = etree_to_string(tree_html.xpath(xpath_tid))
            #获取各相册的total_num
            xpath_total_num = '//*[@class="grbm_ele_a grbm_ele_big"]/span/text()'
            others_total_num = etree_to_string(tree_html.xpath(xpath_total_num))
            
            album_name.extend(others_name)
            album_tid.extend(others_tid)
            album_total_num.extend(others_total_num)
    
    list_sub_album = []
#    print len(album_name)
    for i in xrange(len(album_name)):
        list_sub_album.append((album_name[i], album_tid[i][3:], album_total_num[i]))
    for album_name, tid, total_num in list_sub_album:
        '''从这可以建立相册目录'''
        album_path = '%s/%s吧相册/%s/%s/' % (BASE_PATH, TIEBA_KW, base_name, album_name)
        mkdir(album_path.decode('utf-8'))
        print "----" + album_name
        dlurl = 'http://tieba.baidu.com/photo/g/bw/picture/list?kw=%s&tid=%s&ps=1&pe=%s' % (TIEBA_KW, tid, total_num)
        hjson = s.get(dlurl, headers = headers).json()
        list_pic = []
        pic_list = hjson['data']['pic_list']
        len_pic = len(pic_list)
        for i in xrange(len_pic):
            list_pic.append((pic_list[i]['index'], pic_list[i]['purl']))
        for index_id, purl in list_pic:
            pass
            '''从这建立文件名'''
            #通过pic的下载链接进行图片下载
            index = validateTitle(str(index_id).decode('utf-8'))
            local = u'%s%s.jpg' % (album_path.decode('utf-8'), index)
            if not os.path.exists(r'%s' % local):
                with open(local, 'wb+') as f:
                    f.write(s.get(purl, headers = headers).content)
                    print u"--------" + local + u"...下载完成"
            else:
                print u"--------" + local + u"...已下载"
    
    