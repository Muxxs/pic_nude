#coding=utf-8

import nude,urllib,re,os,threading
from nude import Nude
import uniout
def nude_yesorno(num):
    res=nude.is_nude(str(num)+'.jpg')
    return res


# coding=utf-8
"""根据搜索词下载百度图片"""
import re
import sys
import urllib
import requests

def panduan(bigest):
    for i in range(1,bigest):
        if nude_yesorno(i)==False:
            os.remove(str(i)+".jpg")

def get_onepage_urls(onepageurl):
    """获取单个翻页的所有图片的urls+当前翻页的下一翻页的url"""
    if not onepageurl:
        print('已到最后一页, 结束')
        return [], ''
    try:
        html = requests.get(onepageurl).text
    except Exception as e:
        print(e)
        pic_urls = []
        fanye_url = ''
        return pic_urls, fanye_url
    pic_urls = re.findall('"objURL":"(.*?)",', html, re.S)
    fanye_urls = re.findall(re.compile(r'<a href="(.*)" class="n">下一页</a>'), html, flags=0)
    fanye_url = 'http://image.baidu.com' + fanye_urls[0] if fanye_urls else ''
    return pic_urls, fanye_url


def down_pic(pic_urls):
    """给出图片链接列表, 下载所有图片"""
    bigest=0
    wrong=0
    for i, pic_url in pic_urls:
        try:
            pic = requests.get(pic_url, timeout=15)
            string = str(i + 1) + '.jpg'
            with open(string, 'wb') as f:
                f.write(pic.content)
                print('成功下载第%s张图片: %s' % (str(i + 1), str(pic_url)))
        except Exception as e:
            print('下载第%s张图片时失败: %s' % (str(i + 1), str(pic_url)))
            print(e)
            wrong=wrong+1
            continue
        if i>bigest:
            bigest=i

if __name__ == '__main__':
    keyword = '美女'  # 关键词, 改为你想输入的词即可, 相当于在百度图片里搜索一样
    url_init_first = r'http://image.baidu.com/search/flip?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1497491098685_R&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&ctd=1497491098685%5E00_1519X735&word='
    url_init = url_init_first + urllib.quote(keyword, safe='/')
    all_pic_urls = []
    onepage_urls, fanye_url = get_onepage_urls(url_init)
    all_pic_urls.extend(onepage_urls)

    fanye_count = 0  # 累计翻页数
    while 1:
        onepage_urls, fanye_url = get_onepage_urls(fanye_url)
        fanye_count += 1
        print('第%s页' % fanye_count)
        if fanye_url == '' and onepage_urls == []:
            break
        all_pic_urls.extend(onepage_urls)
    The_list=list(set(all_pic_urls))
    x=1
    a=[]
    for i in The_list:
        word=[x,i]
        x=x+1
        a.append(word)
    The_list=a
    all_num=The_list[-1][0]
    num=int(The_list[-1][0])//4
    print "共"+str(all_num)+"张图片"
    list1=The_list[0:num]
    list2=The_list[num:2*num]
    list3=The_list[2*num:3*num]
    list4=The_list[3*num:-1]
    threads = []
    t1 = threading.Thread(target=down_pic, args=(list1,))
    threads.append(t1)
    t2 = threading.Thread(target=down_pic, args=(list2,))
    threads.append(t2)
    t3 = threading.Thread(target=down_pic, args=(list3,))
    threads.append(t3)
    t4 = threading.Thread(target=down_pic, args=(list4,))
    threads.append(t4)
    for t in threads:
        t.setDaemon(True)
        t.start()
    for t in threads:
        t.join()
    print "over"
    global wrong
    print "共"+str(wrong)+"张下载失败"
    #down_pic(list(set(all_pic_urls)))