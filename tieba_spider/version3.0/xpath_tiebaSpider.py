# coding=utf-8

import urllib.request
import urllib.parse
from lxml import etree
import os


class TiebaSpider(object):
    def __init__(self):
        """
             初始化请求头
        """
        self.header = {
            # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "connection":"keep-alive",
            "User-Agent":"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1 Trident/5.0;"
        }
        self.i = 0
        self.path = "./"

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
    def start(self):
        fileName = input("请输入保存的文件名：")
        for temp in self.pageList:
            page = "&pn=" + str((temp - 1) * 50)
            url = self.url + page
            request = urllib.request.Request(url, headers=self.header)
            response = urllib.request.urlopen(request)
            html = response.read()
            self.handFile(html,fileName)

    def handFile(self,data,fileName):
        """
            处理爬取的内容
        """
        html = etree.HTML(data)
        link_list = html.xpath('//div[@class="threadlist_lz clearfix"]/div/a[@rel="noreferrer"]/@href')
        for temp in link_list:
            link = "http://tieba.baidu.com" + temp
            request = urllib.request.Request(link, headers=self.header)
            # request.add_header("User:Agent", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3534.4 Safari/537.36")
            response = urllib.request.urlopen(request).read()
            img_html = etree.HTML(response)
            img_link_list = img_html.xpath('//div[@class="d_post_content j_d_post_content  clearfix"]//img/@src')
            self.save(img_link_list,fileName)

    def save(self,img_link_link,fileName):
        """
            保存文件
        """
        dirlist = os.listdir("./")
        if "image" in dirlist:
            self.path = "./image/"
        else:
            os.mkdir("image")
            self.path = "./image/"

        for url in img_link_link:
            print(url)
            self.i += 1
            fileWrite = self.path + fileName + str(self.i) + url[-4:]
            file = open(fileWrite, "wb")
            request = urllib.request.Request(url,headers=self.header)
            response = urllib.request.urlopen(request).read()
            file.write(response)
        # data = str(data,encoding="utf-8")
        # file.close()
            file.close()

def main():
    #创建贴吧爬虫对象
    tiebaSpider = TiebaSpider()
    #要爬的贴吧
    name = input("你即将对贴吧进行爬虫，请输入想爬取的贴吧名：")
    tiebaSpider.tiebaName(name)
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
    #开始爬
    tiebaSpider.start()
    print("谢谢使用！")

if __name__ == "__main__":
    main()