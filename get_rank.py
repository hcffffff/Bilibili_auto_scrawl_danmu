from bs4 import BeautifulSoup
import requests
import sys
import re
import time

def get_list():
    m = str(input("你想获取多少天内的数据?('o'-当天,\
        't'-三日,'w'-当周,'m'-当月,不回复自动获取三日数据):"))
    add = ''
    if m == 'o':
        add = '/all/0/0/1'
    elif m == 't':
        add = '/all/0/0/3'
    elif m == 'w':
        add = '/all/0/0/7'
    elif m == 'm':
        add = '/all/0/0/30'

    url = 'https://www.bilibili.com/ranking' + add
    r = requests.get(url)
    
    video_list = re.findall('/BV.*?"',r.text)
    distinct_list = []
    # 去重
    [distinct_list.append(i.replace('/','').replace('"','')) for i in video_list \
                        if not i.replace('/','').replace('"','') in distinct_list]
    print(len(distinct_list))
    return distinct_list

if __name__ == '__main__':
    get_list()


