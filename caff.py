import requests

from lxml import etree
import json
import random


with open('proxies.json', 'r') as f:  # 将代理读取进列表
    proxy_pool = f.readlines()
proxies = json.loads(random.choice(proxy_pool))  # 随机选取一个代理
#匹配获得url
def get_url(url,proxies=proxies):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
    }

    response = requests.get(url,headers=headers,proxies=proxies)
    parseHtml = etree.HTML(response.text)
    url_list = parseHtml.xpath('//li[@class="item"]//a/@href')
    return url_list


#匹配处理文本信息
def parse(list):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
    }

    mmm = {}
    for url in list:
        response = requests.get(url, headers=headers)
        response.encoding = 'gbk2312'
        parseHtml = etree.HTML(response.text)
        title = parseHtml.xpath('/html/body/div[4]/div[1]/div/div[1]/div[1]/div/h1/span/text()')
        p = parseHtml.xpath('/html/body/div[4]/div[1]/div/div[1]/div[1]/div/div[2]/p/text()')
        for i in title:
            mmm[i] = str(p)
    return mmm

def write(mes):
    with open('caff.txt', 'a', encoding='utf-8') as f:
        for each in mes:
            f.write(each + '    ' + mes[each] + '\n')
            f.write('-------------------------------------------------------------------------' + '\n')

def main():
    url = 'https://pythoncaff.com/docs/tutorial/3.7.0'
    html = get_url(url)
    mes = parse(html)
    write(mes)

if __name__ == '__main__':
    main()