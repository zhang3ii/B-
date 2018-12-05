import requests
from bs4 import BeautifulSoup
from lxml import etree
import time
import json
import random


with open('1.json', 'r') as f:  # 将代理读取进列表
    proxy_pool = f.readlines()
proxies = json.loads(random.choice(proxy_pool))  # 随机选取一个代理
#匹配获得url
def get_url(url,proxies=proxies):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
    }

    response = requests.get(url, headers=headers,proxies=proxies)
    parseHtml = etree.HTML(response.text)
    url_list = parseHtml.xpath('//div[@class="w"]//a/@href')
    return url_list[2:-200]


#匹配处理文本信息
def parse(list):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
    }

    mmm = {}
    for url in list:
        response = requests.get(url, headers=headers, proxies=proxies)
        parseHtml = etree.HTML(response.text)

        soup = BeautifulSoup(response.text, 'lxml')
        title = soup.find('h1', class_="title")
        a = title
        if a is None:
            continue
        mes = ''

        for p in soup.select("#Article p"):
            b = p.get_text()
            mes += b
        mmm[(a.string)] = mes
    return mmm

def write(mes):
    with open('my.txt', 'a', encoding='utf-8') as f:
        for each in mes:
            f.write(each + '    ' + mes[each] + '\n')
            f.write('-------------------------------------------------------------------------' + '\n')



def main():
    url = 'http://www.iplaypy.com/'
    html = get_url(url)
    mes = parse(html)
    write(mes)

if __name__ == '__main__':
    main()