import requests
from bs4 import BeautifulSoup
import os
import os.path
import time
import random
import json

headers = {'Referer': 'http://www.mmjpg.com/',
           "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}

with open('1.json', 'r') as f:  # 将代理读取进列表
    proxy_pool = f.readlines()
proxies = json.loads(random.choice(proxy_pool))  # 随机选取一个代理
print('本次使用代理为：' + str(proxies))


def get_text(url, cont=False, proxies=proxies):  # 获取网页的text或者content
    r = requests.get(url, headers=headers, proxies=proxies)
    r.encoding = 'utf-8'
    if cont == True:
        h = r.content
    else:
        h = r.text
    return h


def load_one_folder(url):  # 下载单个系列的所有图片
    folder_text = get_text(url)
    folder_soup = BeautifulSoup(folder_text, 'lxml')
    dirname = folder_soup.h2.string
    index = url[24:]  # 该系列的id
    print('正在保存：' + index + '：' + dirname)
    print('网址为：' + url)

    if not os.path.exists(index + '：' + dirname):  # 文件夹以id+标题的形式命名
        os.mkdir(index + '：' + dirname)
    else:
        pass
    page_num = folder_soup.find(id='page')
    a = page_num.find_all('a')
    max = int(a[-2].string)  # 该系列下的页面总数
    print('本系列一共有' + str(max) + '张图')
    for i in range(1, max + 1):
        img_url = url + '/' + str(i)  # 构造单张图片的网址
        img_text = get_text(img_url)
        s = BeautifulSoup(img_text, 'lxml')
        content = s.find_all(id='content')
        for c in content:
            img = c.find('img')
            src = img['src']  # 高清无码大图地址
            print('正在保存' + src)
            content = get_text(src, True)  # 获取图片二进制文件
            with open(index + '：' + dirname + '\\' + src.split('/')[-1], 'wb')as f:
                f.write(content)
    print('——' * 30)  # 分隔符


def main(i=1):  # 参数为开始的网址ID，默认为1
    base_url = 'http://www.mmjpg.com/mm/'
    try:
        while True:
            folder_url = base_url + str(i)
            load_one_folder(folder_url)
            i += 1
    except:
        with open('i.txt', 'w') as f:  # 创建文件夹保存断点处的网址ID
            f.write(str(i))
        print('本次爬取在' + folder_url + '处中断，中断原因可能为IP被封，现在为您切换Uers-Agent。您也可以手动结束本程序，下次启动时将会从中断处的网址继续爬取。')
        proxies = json.loads(random.choice(proxy_pool))  # 随机更换一个代理
        print('本次使用代理为：' + str(proxies))
        main(i)


if __name__ == '__main__':
    if 'i.txt' in os.listdir('.'):  # 在当前文件夹下寻找i.txt文件，如果有的话，读取里面的值，接着上次发生中断的网址继续爬取
        with open('i.txt', 'r') as f:
            i = int(f.read())
            main(i)
    else:  # 如果没有，那么默认从第一个网址开始
        main()