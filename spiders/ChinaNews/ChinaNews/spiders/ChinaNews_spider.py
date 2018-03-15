# -*-coding:utf-8-*-
__author__ = '陈强'

import scrapy
import json
from ..items import ChinanewsItem
import copy
import re
from bs4 import BeautifulSoup
import jieba.analyse
import time
import datetime

class ChinaNewsSpider(scrapy.Spider):
    name = "ChinaNews"
    # allowed_domains = ["dmoz.org"]
    now = int(time.time()*1000)   #时间戳

    #新闻类型字典
    classification_dict = {'gn':'时政','gj':'国际','sh':'社会','cj':'财经','business':'产经','fortune':'金融','auto':'汽车','ga':'港澳','tw':'台湾','hr':'华人','yl':'娱乐','ty':'体育','cul':'文化','life':'生活','ll':'理论'}

    start_urls = [
        "http://channel.chinanews.com/cns/s/channel:gn.shtml?pager=0&pagenum=20&_=" + str(now),         #时政
        "http://channel.chinanews.com/cns/s/channel:gj.shtml?pager=0&pagenum=20&_=" + str(now),         #国际
        "http://channel.chinanews.com/cns/s/channel:sh.shtml?pager=0&pagenum=20&_=" + str(now),         #社会
        "http://channel.chinanews.com/cns/s/channel:cj.shtml?pager0&pagenum=20&_=" + str(now),          #财经
        "http://channel.chinanews.com/cns/s/channel:business.shtml?pager=0&pagenum=20&_=" + str(now),   #产经
        "http://channel.chinanews.com/cns/s/channel:fortune.shtml?pager=0&pagenum=20&_=" + str(now),    #金融
        "http://channel.chinanews.com/cns/s/channel:auto.shtml?pager=0&pagenum=20&_=" + str(now),    #汽车
        "http://channel.chinanews.com/cns/s/channel:ga.shtml?pager=0&pagenum=20&_=" + str(now),     #港澳
        "http://channel.chinanews.com/cns/s/channel:tw.shtml?pager=0&pagenum=20&_=" + str(now),     #台湾
        "http://channel.chinanews.com/cns/s/channel:hr.shtml?pager=0&pagenum=20&_=" + str(now),     #华人
        "http://channel.chinanews.com/cns/s/channel:yl.shtml?pager=0&pagenum=20&_=" + str(now),    #娱乐
        "http://channel.chinanews.com/cns/s/channel:ty.shtml?pager=0&pagenum=20&_=" + str(now),    #体育
        "http://channel.chinanews.com/cns/s/channel:cul.shtml?pager=0&pagenum=20&_=" + str(now),  #文化
        "http://channel.chinanews.com/cns/s/channel:life.shtml?pager=0&pagenum=20&_=" + str(now),  # 生活
        "http://channel.chinanews.com/cns/s/channel:ll.shtml?pager=0&pagenum=20&_=" + str(now),  # 理论

    ]

    # def start_requests(self):
    #     for i in range(10):
    #         item = ChinanewsItem()
    #
    #         yield scrapy.Request('http://channel.chinanews.com/cns/s/channel:gn.shtml?pager=1&pagenum=20&_=1517296490457', self.parse)
    #

    def parse(self, response):
        text = response.body_as_unicode()
        #伪json数据，对它进行修改变为json数据
        datas = json.loads(text.replace('var specialcnsdata = ','').replace('\r','').replace('\n','')[:-1])
        docs = datas['docs']
        for doc in docs:
            item = ChinanewsItem()
            key = re.findall(r'channel:([a-zA-Z]+)\.shtml',response.url)[0]
            item['classification'] = self.classification_dict[key]
            item['news_link'] = doc['url']

            item['pubtime'] = datetime.datetime.strptime(doc['pubtime'],'%Y-%m-%d %H:%M')

            item['title'] = doc['title']
            item['source'] = '中国新闻网'
            item['abstract'] = doc['content']
            url = doc['url']
            # print(url)
            yield scrapy.Request(url=url,meta={'item':copy.deepcopy(item)},callback=self.parse_news)

        # print(data)
        # json_data = json.loads(data)
        # print(json_data)

    def parse_news(self,response):
        item = response.meta['item']

        soup = BeautifulSoup(response.body_as_unicode(),'html.parser')    #测试发现BeautifulSoup提取p标签内容更准确和简单
        divs = soup.find('div',attrs={'class':'left_zw'})
        content = re.sub(r'\(function\(\) (.|\n)*\(\);','',divs.text)    #去掉里面的广告部分
        # print(content)
        # print(divs)
        # div = response.selector.xpath('//*[@id="cont_1_1_2"]/div[6]')
        # content = ''
        # for p in div.xpath('.//p/text()'):
        #     content += p.extract()
        # # if not str:
        # #     print(response.url)
        # # content = re.sub(r'\(function\(\) (.|\n)*','',str)
        jieba_content = re.sub(r'[0-9]+','',content)     #去掉数字，避免数字被提为关键字
        html_content = re.sub(r'\(function\(\) (.|\n)*\(\);','',str(divs))
        images = re.findall(r'img.*src="(http.*\.jpg)"',html_content)
        image = ''
        for i in images:
            image += i + ','

        tags = jieba.analyse.extract_tags(jieba_content, topK=5, withWeight=False, allowPOS=())
        tag = ''
        for i in tags:
            tag += i + ','
        item['content'] = content
        item['html_content'] = html_content
        item['image'] = image
        item['tag'] = tag
        # print(item)
        yield item

