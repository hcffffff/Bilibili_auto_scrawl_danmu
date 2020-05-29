# Bilibili_auto_scrawl_danmu
简单的程序实现爬取bilibili视频弹幕，排行榜，并制作词云图，绘制高能曲线。
## 使用方法
   * 用到的第三方库: bs4, requests, wordcloud, jieba, matplotlib, scipy, numpy
   * 下载全部文件
   * 运行 main.py 并按照提示操作即可
## 思想
   * 利用bilibili官方API能得到单个视频的近期弹幕内容
   * 爬取网页排行榜可以获得视频的<bv>号
   * 通过<bv>可以爬取弹幕内容
   * 将视频时长分为一定数量的窗口，统计窗口内的弹幕数量可以大致绘制高能曲线
   * 对视频弹幕作词云分析可以绘制词云图
   * 将排行榜上的视频弹幕汇总可得到总的词云图
