from bs4 import BeautifulSoup
import requests
import sys
import re
import time
import get_rank
import analyse
import shutil
import os

header = {
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Referer': 'http://www.bilibili.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:45.0) Gecko/20100101 Firefox/45.0'
}

def get_danmuku(cid, filename, duration):
    try:
        danmuku_api = "https://api.bilibili.com/x/v1/dm/list.so?oid="
        r2 =requests.get(danmuku_api+cid, headers=header)
        soup = BeautifulSoup(r2.content, 'lxml')
        danmus = soup.find_all('d')
        with open(filename, 'w') as f:
            f.write(str(duration)+'\n')
            print(u"写入弹幕")
            for danmu in danmus:
                content = danmu.string
                # 去掉高级弹幕
                if content.find('[') >= 0:
                    continue
                attr = danmu['p'].split(',')
                t1 = str(attr[0]).split('.',1)[0]  # 视频中的时间
                f.write(t1 + ',' + content + '\n')
        print("写入完成...")
    except Exception as e:
        print('写入弹幕错误:')
        print(e)

def get_cid(BVorEP, is_ep):
    try:
        if is_ep:
            url = "https://www.bilibili.com/bangumi/play/" + BVorEP
        else: url = "https://www.bilibili.com/video/"+BVorEP
        r = requests.get(url, headers=header)
        if is_ep:
            match_list = re.findall('"id":{}.*?"cid":\d*?,'\
                .format(BVorEP.split('ep')[1]), r.text)
        else: match_list = re.findall('"cid":\d*?,', r.text)
        cid = match_list[0][match_list[0].index('cid')+5:-1]
        # 获取视频时长
        duration = int(re.findall('"duration":\d*?,',\
             r.text)[0].split(':')[1].replace(',',''))
        return cid, duration
    except Exception as e:
        print('获得cid出错:')
        print(e)
        print(BVorEP)

def get_input_info():
    BV = str(input("请输入想要爬取信息的BV或ep号，以BV或ep开头："))
    return BV

def main(BVorEP):
    is_ep = False
    if str(BVorEP).find('ep') >= 0:
        is_ep = True
    filename = str(sys.path[0])+'/temp_danmuku/{}.txt'.format(BVorEP)
    cid, duration = get_cid(BVorEP, is_ep)
    # print(duration)
    get_danmuku(cid, filename, duration)
    
if __name__ == '__main__':
    # 清空文件夹
    shutil.rmtree(str(sys.path[0]+'/temp_danmuku/'))
    os.mkdir(str(sys.path[0]+'/temp_danmuku/'))
    shutil.rmtree(str(sys.path[0]+'/danmuWC/'))
    os.mkdir(str(sys.path[0]+'/danmuWC/'))
    shutil.rmtree(str(sys.path[0]+'/danmuTimeline/'))
    os.mkdir(str(sys.path[0]+'/danmuTimeline/'))

    rank_list = get_rank.get_list()

    all_danmu_result_jieba = ''
    i = 1
    video_num = len(rank_list)
    for bvstring in rank_list[:]:
        print('开始第{num}个视频，还剩{remaining_num}个视频'\
            .format(num = i,remaining_num = video_num - i))
        main(bvstring)
        analyse.generateTimeLine(bvstring)
        all_danmu_result_jieba += analyse.generateWordCloud(bvstring)
        i += 1

    analyse.makeWordcloudForAll(all_danmu_result_jieba)
    print("写入和分析所有弹幕完成！")