# encoding=utf-8
import re
import datetime
from scrapy.spider import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from Sina_spider1.items import InformationItem, TweetsItem, FollowsItem, FansItem, ReposterItem, NameItem
import time
import os
import logging

logger = logging.getLogger("Sina spider")

class Spider(CrawlSpider):
    name = "sinaSpider"
    host = "http://weibo.cn"
    start_urls = [
        1659553111, 
        1798750043, 
        1698264705,
        # 1739421685

    ]

    website_possible_httpstatus_list = [302]
    handle_httpstatus_list = [403]

    # 记录开始ID
    start_ID = set(start_urls)
    # 记录开始已爬ID

    # 记录待爬tweeturl
    starturllist = set()
    # 记录已爬tweeturl
    finishurllist = set()

    tweetlist = set()
    finishtweetlist = set()

    reposterlist = set()
    finishreposterlist = set()

    retweetlist = set()
    finishretweetlist = set()

    # 数据流向：srartID -> tweetlist -> starturllist -> retweetlist -> reposterlist

    def start_requests(self):
        log = "start from " + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + "\r\n"

        while self.start_ID.__len__():
            # 爬页码
            ID = self.start_ID.pop()
            ID = str(ID)
            self.reposterlist.add(ID)
            url_tweets = "http://weibo.cn/%s/profile?filter=1&page=1" % ID
            yield Request(url=url_tweets, meta={"ID": ID, "through":True}, callback=self.parse6)

        while self.tweetlist.__len__():
                # 爬转发微博URL
                pageurl = self.tweetlist.pop()
                self.finishtweetlist.add(pageurl)
                yield Request(url=pageurl, callback=self.parse2)

        for i in range(400):
            specialurl = "http://weibo.cn/u/13244324234234"
            yield Request(url = specialurl + str(i))


        while self.tweetlist.__len__() or self.starturllist.__len__() or self.reposterlist.__len__() or self.retweetlist.__len__():
            if self.tweetlist.__len__():
                # 爬转发微博URL
                pageurl = self.tweetlist.pop()
                self.finishtweetlist.add(pageurl)
                yield Request(url=pageurl, callback=self.parse2)

            elif self.starturllist.__len__():
                # 爬转发微博页码
                pageurl = self.starturllist.pop()
                self.finishurllist.add(pageurl)
                yield Request(url=pageurl, meta={"url": pageurl}, callback=self.parse7)

            elif self.retweetlist.__len__():
                # 爬转发者
                url = self.retweetlist.pop()
                self.finishretweetlist.add(url)
                url_retweet = url
                yield Request(url=url_retweet, meta={"url": url_retweet}, callback=self.parse4)

            elif self.reposterlist.__len__():
                # 爬个人信息
                ID = self.reposterlist.pop()
                self.finishreposterlist.add(ID)
                ID = str(ID)
                url_information0 = "http://weibo.cn/attgroup/opening?uid=%s" % ID
                yield Request(url=url_information0, meta={"ID": ID}, callback=self.parse0)



        try:
            fo = open(os.getcwd()+"/log.txt", "wb")
            log = log + "end at "+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + "\r\n"
            fo.write(log)
        except:
            pass


    def parse0(self, response):
        if response.body == "":
            req = response.request
            req.meta["change_proxy"] = True
            yield req
        else:
            """ 抓取个人信息1 """
            informationItems = InformationItem()
            selector = Selector(response)
            text0 = selector.xpath('body/div[@class="u"]/div[@class="tip2"]').extract_first()
            if text0:
                # 当给出的正则表达式中带有一个括号时，列表的元素为字符串，此字符串的内容与括号中的正则表达式相对应（不是整个正则表达式的匹配内容）。
                num_tweets = re.findall(u'\u5fae\u535a\[(\d+)\]', text0)  # 微博数
                num_follows = re.findall(u'\u5173\u6ce8\[(\d+)\]', text0)  # 关注数
                num_fans = re.findall(u'\u7c89\u4e1d\[(\d+)\]', text0)  # 粉丝数
                if num_tweets:
                    informationItems["Num_Tweets"] = int(num_tweets[0])
                if num_follows:
                    informationItems["Num_Follows"] = int(num_follows[0])
                if num_fans:
                    informationItems["Num_Fans"] = int(num_fans[0])
                informationItems["_id"] = response.meta["ID"]
                url_information1 = "http://weibo.cn/%s/info" % response.meta["ID"]
                yield informationItems
                # yield Request(url=url_information1, meta={"item": informationItems}, callback=self.parse1)

    def parse1(self, response):
        if response.body == "":
            req = response.request
            req.meta["change_proxy"] = True
            yield req
        else:
            """ 抓取个人信息2 """
            informationItems = response.meta["item"]
            selector = Selector(response)
            # Python join() 方法用于将序列中的元素以指定的字符连接生成一个新的字符串。
            # str = "-";
            # seq = ("a", "b", "c"); # 字符串序列
            # print str.join( seq );
            # a-b-c
            text1 = ";".join(selector.xpath('body/div[@class="c"]/text()').extract())  # 获取标签里的所有text()
            # \uff1a = :
            nickname = re.findall(u'\u6635\u79f0[:|\uff1a](.*?);', text1)  # 昵称
            gender = re.findall(u'\u6027\u522b[:|\uff1a](.*?);', text1)  # 性别
            place = re.findall(u'\u5730\u533a[:|\uff1a](.*?);', text1)  # 地区（包括省份和城市）
            signature = re.findall(u'\u7b80\u4ecb[:|\uff1a](.*?);', text1)  # 个性签名
            birthday = re.findall(u'\u751f\u65e5[:|\uff1a](.*?);', text1)  # 生日
            sexorientation = re.findall(u'\u6027\u53d6\u5411[:|\uff1a](.*?);', text1)  # 性取向
            marriage = re.findall(u'\u611f\u60c5\u72b6\u51b5[:|\uff1a](.*?);', text1)  # 婚姻状况
            url = re.findall(u'\u4e92\u8054\u7f51[:|\uff1a](.*?);', text1)  # 首页链接

            if nickname:
                informationItems["NickName"] = nickname[0]
            if gender:
                informationItems["Gender"] = gender[0]
            if place:
                place = place[0].split(" ")
                informationItems["Province"] = place[0]
                if len(place) > 1:
                    informationItems["City"] = place[1]
            if signature:
                informationItems["Signature"] = signature[0]
            if birthday:
                try:
                    birthday = datetime.datetime.strptime(birthday[0], "%Y-%m-%d")
                    informationItems["Birthday"] = birthday - datetime.timedelta(hours=8)
                except Exception:
                    pass
            if sexorientation:
                if sexorientation[0] == gender[0]:
                    informationItems["Sex_Orientation"] = "gay"
                else:
                    informationItems["Sex_Orientation"] = "Heterosexual"
            if marriage:
                informationItems["Marriage"] = marriage[0]
            if url:
                informationItems["URL"] = url[0]
            yield informationItems

    def parse2(self, response):
        """ 抓取微博数据 """
        if response.body == "":
            req = response.request
            req.meta["change_proxy"] = True
            yield req
        else:
            # logger.info("got page: %s" % response.body)

            selector = Selector(response)
            urllist = selector.xpath('//a[@href]/@href').extract()
            for text00 in urllist:
                reposturl = re.findall(r'^http://weibo.cn/repost/',text00)
                if reposturl:
                    if text00 not in self.finishurllist:
                        self.starturllist.add(text00)            

            # 爬取ID
            text7 = selector.xpath('body/div[@class="u"]/div[@class="tip2"]').extract_first()
            if text7:
                ID = re.findall('uid=(\d+)', text7)[0]

            tweets = selector.xpath('body/div[@class="c" and @id]')
            for tweet in tweets:
                tweetsItems = TweetsItem()
                id = tweet.xpath('@id').extract_first()  # 微博ID
                content = tweet.xpath('div/span[@class="ctt"]/text()').extract_first()  # 微博内容
                cooridinates = tweet.xpath('div/a/@href').extract_first()  # 定位坐标
                like = re.findall(u'\u8d5e\[(\d+)\]', tweet.extract())  # 点赞数
                transfer = re.findall(u'\u8f6c\u53d1\[(\d+)\]', tweet.extract())  # 转载数
                comment = re.findall(u'\u8bc4\u8bba\[(\d+)\]', tweet.extract())  # 评论数
                others = tweet.xpath('div/span[@class="ct"]/text()').extract_first()  # 求时间和使用工具（手机或平台）



                tweetsItems["ID"] = ID
                tweetsItems["_id"] = ID + "-" + id
                tweetsItems["tweetID"] = id 
                if content:
                    tweetsItems["Content"] = content.strip(u"[\u4f4d\u7f6e]")  # 去掉最后的"[位置]"
                if cooridinates:
                    cooridinates = re.findall('center=([\d|.|,]+)', cooridinates)
                    if cooridinates:
                        tweetsItems["Co_oridinates"] = cooridinates[0]
                if like:
                    tweetsItems["Like"] = int(like[0])
                if transfer:
                    tweetsItems["Transfer"] = int(transfer[0])
                if comment:
                    tweetsItems["Comment"] = int(comment[0])
                if others:
                    others = others.split(u"\u6765\u81ea")
                    tweetsItems["PubTime"] = others[0]
                    if len(others) == 2:
                        tweetsItems["Tools"] = others[1]
                yield tweetsItems
                # @href内容构成新的一页
        # url_next = selector.xpath(
        #     u'body/div[@class="pa" and @id="pagelist"]/form/div/a[text()="\u4e0b\u9875"]/@href').extract()
        # if url_next:
        #     yield Request(url=self.host + url_next[0], meta={"ID": response.meta["ID"]}, callback=self.parse2)

    def parse3(self, response):
        if response.body == "":
            req = response.request
            req.meta["change_proxy"] = True
            yield req
        else:
            """ 抓取关注或粉丝 """
            items = response.meta["item"]
            selector = Selector(response)
            text2 = selector.xpath(
                u'body//table/tr/td/a[text()="\u5173\u6ce8\u4ed6" or text()="\u5173\u6ce8\u5979"]/@href').extract()
            for elem in text2:
                elem = re.findall('uid=(\d+)', elem)
                if elem:
                    # result实际上是FANS
                    response.meta["result"].append(elem[0])
                    ID = int(elem[0])
                    if ID not in self.finish_ID:  # 新的ID，如果未爬则加入待爬队列
                        self.scrawl_ID.add(ID)
            url_next = selector.xpath(
                u'body//div[@class="pa" and @id="pagelist"]/form/div/a[text()="\u4e0b\u9875"]/@href').extract()
            if url_next:
                yield Request(url=self.host + url_next[0], meta={"item": items, "result": response.meta["result"]},
                              callback=self.parse3)
            else:  # 如果没有下一页即获取完毕
                yield items

    def parse4(self, response):
        # 抓取转发者
        if response.body == "":
            req = response.request
            req.meta["change_proxy"] = True
            yield req
        else:
            reposturl = response.meta['url']
            ID = re.findall('uid=(\d+)', reposturl)

            reposturl = reposturl.lstrip('http://weibo.cn/repos')
            reposturl = reposturl.lstrip('t')
            reposturl = reposturl.lstrip('/')
            tweetID = re.findall('(.+)\?',reposturl)[0]
            tweetID = str(tweetID)

            reposters = []
            repostersItems = ReposterItem()
            repostersItems['_id'] = str(ID) + '-' + str(tweetID) 
            repostersItems['ID'] = ID
            repostersItems['tweetID'] = tweetID

            selector = Selector(response)
            text3 = selector.xpath('//div[@class="c"]/a[1]/@href').extract()
            for elem in text3:
                reposterID = re.findall('^/u/(\d+)',elem)
                if reposterID:
                    reposters.append(reposterID[0])
                    if reposterID[0] not in self.finishreposterlist:
                        self.reposterlist.add(reposterID[0])
                else:
                    reposterID = elem.strip('/')
                    reposters.append(reposterID)

                    mainpageurl = "http://weibo.cn/%s" % reposterID
                    nameItems = NameItem()
                    if reposterID:
                        nameItems["_id"] = reposterID
                    yield Request(url= mainpageurl, meta={"item": nameItems}, callback = self.parse5)

            repostersItems['reposters'] = reposters
            yield repostersItems

            # url_next = selector.xpath(
            #     u'body//div[@class="pa" and @id="pagelist"]/form/div/a[text()="\u4e0b\u9875"]/@href').extract()
            # if url_next:
            #     yield Request(url=self.host + url_next[0], meta={"item": items, "result": response.meta["result"]},
            #                   callback=self.parse4)
            # else:  # 如果没有下一页即获取完毕
            # yield items

    def parse5(self,response):
        if response.body == "":
            req = response.request
            req.meta["change_proxy"] = True
            yield req
        else:
        # 英文域名ID转换
            items = response.meta['item']
            selector = Selector(response)
            text0 = selector.xpath('body/div[@class="u"]/div[@class="tip2"]').extract_first()
            if text0:
                ID = re.findall('uid=(\d+)', text0)[0]
                if ID:
                    ID = str(ID)
                    if ID not in self.finishreposterlist:
                        self.reposterlist.add(ID)
                    items["ID"] = ID
            yield items

    def parse6(self,response):
        if response.body == "":
            req = response.request
            req.meta["change_proxy"] = True
            yield req
        else:
            # 爬取页码
            ID = response.meta['ID']
            selector = Selector(response)
            Num = (int)(selector.xpath('//input[@name="mp"]/@value').extract()[0])
            for page in range (Num+1):
                # print page
                url = 'http://weibo.cn/u/%s?filter=1&page=%d'%(ID,page)
                if url not in self.finishtweetlist:
                    self.tweetlist.add(url)
            return

    def parse7(self,response):
        if response.body == "":
            req = response.request
            req.meta["change_proxy"] = True
            yield req
        else:
            pageurl = response.meta["url"]
            # 爬取页码
            selector = Selector(response)
            try:
                Num = (int)(selector.xpath('//input[@name="mp"]/@value').extract()[0])
            except:
                self.retweetlist.add(pageurl)
                return
            for page in range (Num+1):
                newurl = pageurl + '&page=%d'%(Num)
                if newurl not in self.finishretweetlist:
                    self.retweetlist.add(newurl)
            return



