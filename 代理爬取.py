import requests
import re,json,os
import random
from multiprocessing import Pool
import requests
import time,json

def save_ips(isCover=False):
    """保存所有代理IP的数据"""
    url = "https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list"# github上的开源IP
    r = requests.get(url)
    wb = r.text
    # 处理数据
    proxies = []
    pattern = re.compile(r'{.*?}')
    data = pattern.findall(wb, re.S)
    for d in data:
        dict_obj = json.loads(d)
        if dict_obj["anonymity"] == "high_anonymous":  # 这里我只保存了高匿代理
            temp = {}
            temp["type"] = dict_obj["type"]
            temp["host"] = dict_obj["host"]
            temp["port"] = dict_obj["port"]
            proxies.append(temp)
    # 把代理IP保存下来
    filename = "all_ips.txt"
    path = filename  # 保存文件的路径，这里我直接保存在项目的路径下了
    if isCover == False: # 防止覆盖原有的文件
        if os.path.exists(path):
            print(path,"文件已存在，注意防止覆盖无关文件")
            return
    f = open(path, "w")
    f.write(json.dumps(proxies)) # 以json格式保存数据，方便解析
    f.close()
    print(path,'save succeed')

def get_ips(total=1):
    """读取已经保存的IP，随机抽出total数量的IP"""
    path = "all_ips.txt"
    if os.path.exists(path) == False:
        print(path,"文件不存在")
        return
    f = open(path,'r')
    data = json.load(f)
    f.close()
    http_list = []
    https_list = []
    for i in range(len(data)):
        if data[i]['type'] == 'http':
            http_list.append('http://' + data[i]['host'] + ':' + str(data[i]['port']))
        if data[i]['type'] == 'https':
            https_list.append('https://' + data[i]['host'] + ':' + str(data[i]['port']))
    proxies = []
    for j in range(total):
        http = random.choice(http_list)
        https = random.choice(https_list)
        proxy = {'http':http,'https':https}  # 返回的每一个代理
        proxies.append(proxy)
    return proxies


def my_process(proxies):
    """每个子进程"""
    useful_proxies = []
    url = ""  # 要用代理访问的url
    headers = {
        "Cookies":"",
        "User-Agent":"",
    }   # 请求头，cookies,UA都写在请求头里
    timeout = 2   # 超时设置，可以用来控制代理的速度，像设置为1可以挑选更快的代理
    for proxy in proxies:
        try:
            r = requests.get(url=url,headers=headers,proxies=proxy,timeout=timeout)
            useful_proxies.append(proxy)
        except:
            continue
    return useful_proxies


if __name__ == "__main__":
    s = time.time()
    # 保存所有的IP
    save_ips(isCover=True)
    # 多进程筛选较快的IP
    data = []
    pool = Pool(4)
    result = []
    for i in range(10):
        proxies = get_ips(total=10)
        useful_proxies = pool.apply_async(my_process,args=(proxies,))
        result.append(useful_proxies)
    pool.close()
    pool.join()
    # 将较快的代理保存在data数组中，写入文件
    for r in result:
        for proxy in r.get():
            data.append(proxy)
    path = "screened_ips.txt" # 保存经过初步筛选的代理IP的文件路径
    f = open(path,"w")
    f.write(json.dumps(data))
    f.close()
    print("useful ips save succeed")
    e = time.time()
    print("总时间",e-s)
