import requests
from pyquery import PyQuery as pq
import os, time
from urllib.request import urlretrieve

def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)

def getImgUrl():
    headers = {
        'Host': 'www.tupianzj.com',
        'User - Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                        ' Chrome/75.0.3770.142 Safari/537.36'
    }
    host = 'https://www.tupianzj.com'
    url = 'https://www.tupianzj.com/meinv/'
    urls = []
    res = requests.get(url, headers=headers)
    res.encoding = 'gb2312'
    content = pq(res.text)('.list_title')
    aUrls = []
    aNames = []
    for i in content.items():
        url = i('a').attr('href')
        name = i('a').text().strip()
        # print(name, url)
        aUrls.append(url)
        aNames.append(name)
    bUrls = []
    bNames = []
    for i in aUrls:
        res = requests.get(i, headers=headers)
        res.encoding = 'gb2312'
        content = pq(res.text)('.list_con_box_ul li a')
        for j in content.items():
            # print(j)
            url = host + j('a').attr('href')
            name = j('label').text()
            if name:
                print(name, url)
                bUrls.append(url)
                bNames.append(name)

    return bUrls, bNames


def main():
    headers = {
        'Host': 'www.tupianzj.com',
        'User - Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                        ' Chrome/75.0.3770.142 Safari/537.36'
    }
    host = 'https://m.tupianzj.com'
    url = 'https://www.tupianzj.com/meinv/'
    urls = []
    res = requests.get(url, headers=headers)
    res.encoding = 'gb2312'
    content = pq(res.text)('.list_title')
    for i in content.items():
        aUrl = i('a').attr('href')
        aName = i('a').text().strip()
        # print(aName, aUrl)
        mkdir('D:\\tupianzj\\{}'.format(aName))
        res = requests.get(aUrl, headers=headers)
        res.encoding = 'gb2312'
        content = pq(res.text)('.list_con_box_ul li a')
        for j in content.items():
            # print(j)
            bUrl = host + j('a').attr('href')
            bName = j('label').text()
            if bName:
                # print(bName, bUrl)
                mkdir('D:\\tupianzj\\'+aName+'\\{}'.format(bName))
                index = 1
                while True:
                    if index > 1:
                        bUrl = bUrl.split('_')[0].split('.html')[0]+'_'+str(index)+'.html'
                    index = index + 1
                    res = requests.get(bUrl, headers=headers)
                    res.encoding = 'gb2312'
                    bContent = pq(res.text)('#bigpicimg').attr('src')
                    # print(bContent)
                    if bContent:
                        bPath = 'D:\\tupianzj\\'+aName+'\\'+bName+'\\'+str(index)+'.jpg'
                        if not os.path.exists(bPath):
                            urlretrieve(bContent, bPath)
                            print('{}下载完成'.format(bContent))
                            time.sleep(0.5)
                    else:
                        print(bUrl)
                        break

        

if __name__ == '__main__':
    main()