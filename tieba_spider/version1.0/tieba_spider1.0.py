# coding=utf-8

import urllib.request
import urllib.parse
import random


class TiebaSpider(object):
    #初始化请求头
    def __init__(self):
        self.header = {
            # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "connection":"keep-alive",
        }
        ua_list = [
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
        ]
        self.user_agent = random.choice(ua_list)

    #爬取的贴吧名
    def tiebaName(self,name):
        url = "http://tieba.baidu.com/f?"
        encode = urllib.parse.urlencode({"kw":name})
        self.url = url + encode

    #爬取多少页
    def tiebaPage(self,num):
        self.pageList = []
        for temp in range(1, num+1):
            self.pageList.append(temp)

    #开始爬取
    def start(self,fileName,path="./"):
        for temp in self.pageList:
            page = "&pn=" + str((temp - 1) * 50)
            url = self.url + page
            request = urllib.request.Request(url, headers=self.header)
            request.add_header("User-Agent", self.user_agent)
            response = urllib.request.urlopen(request)
            data = response.read()
            # data = str(data,encoding="utf-8")
            fileWrite = "./" + fileName + str(temp) + ".html"
            file = open(fileWrite, "wb")
            file.write(data)
            file.close()


def main():
    #创建贴吧爬虫对象
    tiebaSpider = TiebaSpider()
    print(1)
    #要爬的贴吧
    name = input("你即将对贴吧进行爬虫，请输入想爬取的贴吧名：")
    tiebaSpider.tiebaName(name)
    print(2)
    #爬多少页
    page = int(input("你想爬多少页："))
    if page >= 50:
        select = input("你想爬取的页面有点多，目前程序比较低级，可能有被贴吧拉入黑名单的风险，需要继续吗（是/否）：")
        if select.count("否"):
            print("该程序不允许后悔！")
        elif len(select) > 1:
            print("输入错误，按默认继续执行")
        else:
            print("按默认执行中！")
    tiebaSpider.tiebaPage(page)
    print(3)
    # 保存文件
    fileName = input("请输入保存的文件名：")
    #开始爬
    tiebaSpider.start(fileName)
    print(4)

if __name__ == "__main__":
    main()