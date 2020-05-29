import jieba
import string
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy as np
import sys
import scipy.signal

def generateWordCloud(bvstring):
    file = str(sys.path[0]) +'/temp_danmuku/{}.txt'.format(bvstring)
    text = open(file, 'r').readlines()[1:]
    danmuList = []
    for line in text:
        if line.find(',') >= 0:
            danmuList.append((line.split(',',1)[1]).strip('\n').replace(' ',''))

    # emoji = r"(?:[^\s])(?<![\w{ascii_printable}])".format(ascii_printable=string.printable)
    # regexp = r"{emoji}".format(emoji=emoji)

    jieba.add_word('卧槽')
    jieba.add_word('高能')
    jieba.add_word('护体')

    result = ''
    for item in danmuList:
        result = result + ('/'.join(jieba.cut(item,cut_all=False)))

    if result == '': # 弹幕可能为空(某些视频不允许发送弹幕)
        return ''

    wc = WordCloud(font_path=str(sys.path[0])+'/simhei.ttf',background_color='white',max_font_size=50)
    wc.generate(result)

    plt.imshow(wc)         # 以图片的形式显示词云
    plt.axis("off")        # 关闭图像坐标系
    # plt.savefig(str(sys.path[0]+'/danmuWC/{}.png'.format(bvstring+'danmuWordCloud')))
    wc.to_file(str(sys.path[0]+'/danmuWC/{}.png'.format(bvstring+'danmuWordCloud')))
    plt.close()
    return result # 返回弹幕分词信息

def generateTimeLine(bvstring):
    file = str(sys.path[0]) +'/temp_danmuku/{}.txt'.format(bvstring)
    duration = int(open(file, 'r').readline().strip('\n'))

    text = open(file, 'r').readlines()[1:]
    timeList = []
    for line in text:
        if line.find(',') >= 0:
            timeList.append(int((line.split(',',1)[0]).strip('\n').replace(' ','')))
        else: continue
    if timeList == None: # 如果弹幕信息为空
        return
    # 设置单位格的时间长度
    item = duration//2 # 设置单元格数量，越多越精确，曲线越平滑，但效果可能减弱
    item_duration = float(duration/item)
    print('该视频时间为:{}s'.format(duration))
    if item > 50:
        window_len = 41
    else: window_len =  item if (item%2==1) else item-1

    timeline = [0 for n in range(item+1)]
    for i in timeList:
        # 分组每个弹幕
        timeline[int(i//item_duration)] += 1
    xtime = [i*item_duration for i in range(item + 1)]
    # 平滑处理
    smooth = scipy.signal.savgol_filter(timeline, window_len, 3)

    l1 = plt.plot(xtime, timeline, '-', label = 'original', color = 'blue')
    l2 = plt.plot(xtime, smooth, '-', label = 'smoothed', color = 'red')
    plt.plot(xtime, timeline, 'b-',xtime, smooth, 'r-')
    plt.title('Fantastic Timeline for {}'.format(bvstring))
    plt.xlabel('timeline(s)')
    plt.ylabel('count')
    plt.legend()
    plt.savefig(str(sys.path[0]+'/danmuTimeline/{}.jpg'.format(bvstring+'timeline')))
    plt.close()
    

def makeWordcloudForAll(string):
    stopwords = set()
    stopwords.update(['哈','哈哈','哈哈哈','哈哈哈哈','啊',
                      '啊啊','啊啊啊','啊啊啊啊','没有','真的',
                      '就是','什么','不是','这么','自己',
                      '不会','这个','怎么','觉得','一个',
                      '有点','那么','你们','一样','还是',
                      '还有','已经','知道','是不是','那个',
                      '可以','不能','时候','感觉','这样',
                      '好像','因为','现在','不要',''])

    wc = WordCloud(font_path=str(sys.path[0])+'/simhei.ttf',stopwords=stopwords,background_color='white',max_font_size=50)
    wc.generate(string)

    plt.imshow(wc)         # 以图片的形式显示词云
    plt.axis("off")        # 关闭图像坐标系
    wc.to_file(str(sys.path[0]+'/all_danmu_wordcloud.png'))
    plt.close()