from scrapy import cmdline
import time
import os


def crawl():
    os.system('scrapy crawl ChinaNews')
    # cmdline.execute('scrapy crawl ChinaNews'.split())

if __name__=='__main__':
    count = 1
    while True:
        crawl()
        print('爬取 ',count,' 次')
        count += 1
        time.sleep(1000)          #1000秒爬取一次，更新数据
