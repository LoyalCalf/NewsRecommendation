# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from twisted.enterprise import adbapi
import pymysql
import pymysql.cursors

class ChinanewsPipeline(object):
    def __init__(self):
        self.file = open("./books.json", "wb")

    def process_item(self, item, spider):
        # 编码的转换
        for k in item:
            item[k] = item[k].encode("utf8")
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item


class MysqlTwistPipeline(object):

    @classmethod
    def from_settings(cls,settings):#名称固定 会被scrapy调用 直接可用setting的值
        adbparams=dict(
            host=settings['MYSQL_HOST'],
            db = settings['MYSQL_DBNAME'],
            user = settings['MYSQL_USER'],
            password = settings['MYSQL_PASSWORD'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
            port=3306
            )
        #这是链接数据库的另一种方法，在settings中写入参数
        dbpool=adbapi.ConnectionPool('pymysql',**adbparams)
        return cls(dbpool)

    def __init__(self,dbpool):
        self.dbpool=dbpool

    def process_item(self, item, spider):
        #使用twiest将mysql插入变成异步
        query=self.dbpool.runInteraction(self.do_insert,item)
        #因为异步 可能有些错误不能及时爆出
        query.addErrback(self.handle_error)

    #处理异步的异常
    def handle_error(self,failure):
        # print('failure')
        pass

    def do_insert(self,cursor,item):
        insert_sql = """
                    insert into news_news(news_link,source,title,pubtime,abstract,content,
                    html_content,image,tag,classification)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """
        cursor.execute(insert_sql, (item['news_link'], item['source'], item['title'], item['pubtime'],item['abstract'], item['content'], item['html_content'],item['image'], item['tag'],item['classification']))