import requests
from pyquery import PyQuery as pq
import os, time
from urllib.request import urlretrieve
import threading
import time
import re

headers = {
    'Host': 'www.tupianzj.com',
    'User - Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                    ' Chrome/75.0.3770.142 Safari/537.36'
}
host = 'https://m.tupianzj.com'

class myThread (threading.Thread):
    def __init__(self, name, url):
        threading.Thread.__init__(self)
        self.name = name
        self.url = url
    def run(self):
        name = self.name
        url = self.url
        print ("开始线程：" + name)
        startTime = time.time()
        while url != '':
            print('开始爬取：' + url)
            if name == '美女专题':
                content = getContent(url, headers, 'gb2312', '.list_con_box_ul div li a')
                for i in content.items():
                    aUrl = i.attr('href')
                    aName = i.attr('title')
                    # print(aName, aUrl)
                    mkdir('D:\\tupianzj\\{}\\{}'.format(name, aName))
                    content = getContent(host + aUrl, headers, 'gb2312', '.ico3 li a')
                    for j in content.items():
                        bUrl = host + j('a').attr('href')
                        bName = j('img').attr('alt')
                        if bName:
                            spider(name+'\\'+aName, bName, bUrl)
            else:
                content = getContent(url, headers, 'gb2312', '.list_con_box_ul li a')
                for i in content.items():
                    bUrl = host + i('a').attr('href')
                    bName = i('label').text()
                    if bName:
                        spider(name, bName, bUrl)
                    
            url = nextPage(url)
        atime = time.time() - startTime
        print ("退出线程：{} 用时：{}".format(name, getFloat(atime, 2)))

def nextPage(url):
    content = getContent(url, headers, 'gb2312', '.pages > ul > li')
    for i in content.items():
        if i.text() == '下一页':
            return url.split('list_')[0] + i('a').attr('href')
    return ""

def spider(aName, bName, bUrl):
    index = 1
    startTime = time.time()
    while True:
        if index > 1:
            bUrl = bUrl.split('_')[0].split('.html')[0]+'_'+str(index)+'.html'
        index = index + 1
        bContent = getContent(bUrl, headers, 'gb2312', '#bigpicimg').attr('src')
        # print(bContent)
        if bContent:
            reg = "[^0-9A-Za-z\u4e00-\u9fa5]"
            bName = re.sub(reg, '', bName)
            bPath = 'D:\\tupianzj\\{}\\{}_{}.jpg'.format(aName, bName, str(index-1))
            if not os.path.exists(bPath):
                urlretrieve(bContent, bPath)
                # print('{} 下载完成'.format(bContent))
                # time.sleep(0.5) 
        else:
            atime = time.time() - startTime
            print('{}\\{}({}) 爬取完毕 用时：{}秒'.format(aName, bName, str(index-1), getFloat(atime, 2)))
            break

def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)

def getFloat(f_str, n):
    f_str = str(f_str)      # f_str = '{}'.format(f_str) 也可以转换为字符串
    a, b, c = f_str.partition('.')
    c = (c+"0"*n)[:n]       # 如论传入的函数有几位小数，在字符串后面都添加n为小数0
    return ".".join([a, c])

def getContent(url, headers, encoding, selector):
    res = requests.get(url, headers=headers)
    res.encoding = encoding
    content = pq(res.text)(selector)
    return content


def main():
    url = 'https://www.tupianzj.com/meinv/'
    content = getContent(url, headers, 'gb2312', '.list_title')
    for i in content.items():
        aUrl = i('a').attr('href')
        aName = i('a').text().strip()
        # print(aName, aUrl)
        mkdir('D:\\tupianzjj\\{}'.format(aName))
        # 开启线程
        if aName == '美女专题':
            myThread(aName, aUrl).start()

if __name__ == '__main__':
    main()
