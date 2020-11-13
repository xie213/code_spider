import requests
from lxml import etree
import pymysql

class Spider_Crawl():
    '''
    数据获取
    '''
    def get_url(self,url):
        # 访问这个网址
        r = requests.get(url)
        # r.encoding = "utf-8"
        r.encoding = r.apparent_encoding
        html = r.text
        return html

    def myself_parse(self, html,x):
        # 提取主页面小说以及url
        r = etree.HTML(html)
        vote_name = r.xpath(x)
        return vote_name


    def parse(self,html):
        # 提取主页面小说以及url
        r = etree.HTML(html)
        # xpath进行匹配

        vote_name = r.xpath("//div[@class = 'novelslist']//li/a/text()")
        #print("小说名:",vote_name)

        vote_url = r.xpath("//div[@class = 'novelslist']//li/a/@href")
        #print("小说url:", vote_url)

        #变成字典的数据
        d = dict(zip(vote_name, vote_url))
        # print('寻找到的数据',d)

        return d

    def detail_parse(self,html):
        # 每一个小说详细章节的匹配 提取、整理
        r = etree.HTML(html)
        # xpath进行匹配

        vote_list_name = r.xpath("//div[@id='list']//dd/a/text()")
        vote_list_url = r.xpath("//div[@id='list']//dd/a/@href")
        # print("详细章节的名称：",vote_list_name)
        # print("详细章节的url：",vote_list_url)

        detail_d = dict(zip(vote_list_name, vote_list_url))
        return detail_d


    def read_parse(self,html):
        # 每一个小说详细章节的匹配 提取、整理
        r = etree.HTML(html)
        content = r.xpath("//div[@id='content']//text()")
        h_str = ""
        for i in content:
            h_str += i
        return h_str


class Save():



    # 构造函数
    def __init__(self):
        self.nn = pymysql.connect(host='127.0.0.1',  # 连接名称，默认127.0.0.1
              user='root',  # 用户名
              password='123456',  # 密码
              port=3306,  # 端口,默认为：3306
              database='spider',  # 数据库名称
              charset='utf8')  # 字符编码

        self.cursor = self.nn.cursor()  # 生成游标（拿数据的手）

    # 查找， 一个参数sql 语句插入
    def Search(self, sql):
        # sql语句
        self.cursor.execute(sql)  # 执行语句
        data = self.cursor.fetchall()  # 通过fetchall方法获得数据
        return data

    def Insert(self, sql):
        # 执行函数
        self.cursor.execute(sql)  # 执行语句

        # 涉及插入数据要注意提交
        self.nn.commit()

    # 关闭
    def Close(self):
        # 关闭光标对象
        self.cursor.close()
        # 关闭数据库连接
        self.nn.close()

if __name__ == '__main__':

    spider = Spider_Crawl()

    #要爬取的网址   获取
    url = "http://www.xbiquge.la/"
    html = spider.get_url(url)
    # print("--------------",html)
    detail_vote = spider.parse(html)
    #s = "http://www.xbiquge.la"
    print("*-----",detail_vote)

    s = Save()

    for key in detail_vote.keys():
        pass
        print(key)
        print(detail_vote[key])
        sql  = "insert into story_name(url,story) value ('{}','{}')".format(detail_vote[key],key)
        s.Insert(sql)

    s.Close()

    # detail_vote = {"全球武道进化":"http://www.xbiquge.la/44/44578/"}
    # for key in detail_vote.keys():
    #     # print(key)
    #     #访问每一个小说
    #     r = spider.get_url(detail_vote[key])
    #     detail_d = spider.detail_parse(r)
    #     # print("--------",detail_d)
    #
    #     for j in detail_d.keys():
    #         # print("**********",detail_d.get(j))
    #         detail_url = s + detail_d.get(j)
    #         print("list:",detail_url)
    #         content_text = spider.get_url(detail_url)
    #         spider.read_parse(content_text)
        # print("------",detail_vote[key])
