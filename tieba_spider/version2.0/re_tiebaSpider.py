# coding=utf-8

import urllib.request
import urllib.parse
import random
import re


class TiebaSpider(object):
    def __init__(self):
        """
             初始化请求头
        """
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
    def start(self):
        fileName = input("请输入保存的文件名：")
        for temp in self.pageList:
            page = "&pn=" + str((temp - 1) * 50)
            url = self.url + page
            request = urllib.request.Request(url, headers=self.header)
            request.add_header("User-Agent", self.user_agent)
            response = urllib.request.urlopen(request)
            html = response.read().decode("utf-8")
            # print(html)
            self.handFile(html,fileName)

    def handFile(self,data,fileName):
        """
            处理爬取的内容
        """
        ret = re.findall(r"""<div\sclass="threadlist_abs\sthreadlist_abs_onlyline\s">\n\s*(.*)\n\s*</div>""", data)
        print(ret)
        self.save(ret,fileName)

    def save(self,data,fileName):
        """
            保存文件
        """
        fileWrite = "./" + fileName + ".txt"
        file = open(fileWrite, "ab")
        for temp in data:
            temp = temp + "\r\n"
            file.write(temp.encode("utf-8"))
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